import numpy as np
import scipy
import scipy.sparse as sp

from ..settings import ProcessSelDataType

from memory_profiler import profile


class TGV_Denoise():

    def __init__(self):

        self.h_inv = 1.0
        self.hz_inv = 1.0

        self.tau_init = 10

    def _make_nabla(self, L, M, N):
        row = np.arange(0, L * M * N)
        dat = np.ones(L * M * N)
        col = np.arange(0, M * N * L).reshape(L, M, N)
        col_xp = np.concatenate([col[:, :, 1:], col[:, :, -1:]], axis=2)
        col_yp = np.concatenate([col[:, 1:, :], col[:, -1:, :]], axis=1)
        col_zp = np.concatenate([col[1:, :, :], col[-1:, :, :]], axis=0)

        # flatten vector contains all the indices for the positions where -1 and 1 should be placed to calculate
        # gradient for every pixel in all 3 dimensions.

        # for every pixel (pixel amount L*M*N) that should be calculated, a sparse vector (length L*M*N) is generated
        # which just contains the 1 and -1 on the
        # specific place and is 0 otherwhise. Thats why its a (L*M*N, L*M*N)
        # matrix

        nabla_x = (
            scipy.sparse.coo_matrix(
                (dat, (row, col_xp.flatten())), shape=(
                    L * M * N, L * M * N)) - scipy.sparse.coo_matrix(
                (dat, (row, col.flatten())), shape=(
                    L * M * N, L * M * N))) * self.h_inv

        nabla_y = (
            scipy.sparse.coo_matrix(
                (dat, (row, col_yp.flatten())), shape=(
                    L * M * N, L * M * N)) - scipy.sparse.coo_matrix(
                (dat, (row, col.flatten())), shape=(
                    L * M * N, L * M * N))) * self.h_inv

        nabla_z = (
            scipy.sparse.coo_matrix(
                (dat, (row, col_zp.flatten())), shape=(
                    L * M * N, L * M * N)) - scipy.sparse.coo_matrix(
                (dat, (row, col.flatten())), shape=(
                    L * M * N, L * M * N))) * self.hz_inv

        nabla = scipy.sparse.vstack([nabla_x, nabla_y, nabla_z])

        return nabla, nabla_x, nabla_y, nabla_z

    def make_K(self, L, M, N):

        nabla, nabla_x, nabla_y, nabla_z = self._make_nabla(L, M, N)
        neg_I = sp.identity(L * M * N) * -1

        K = sp.bmat(
            [
                [
                    nabla_x, neg_I, None, None], [
                    nabla_y, None, neg_I, None], [
                    nabla_z, None, None, neg_I], [
                        None, nabla_x, None, None], [
                            None, nabla_y, None, None], [
                                None, nabla_z, None, None], [
                                    None, None, nabla_x, None], [
                                        None, None, nabla_y, None], [
                                            None, None, nabla_z, None], [
                                                None, None, None, nabla_x], [
                                                    None, None, None, nabla_y], [
                                                        None, None, None, nabla_z]])

        return K

    def prox_G(self, u, f, tau, lambd):

        prox = (f * tau * lambd + u) / (1 + tau * lambd)

        return prox

    def proj_ball(self, Y, alpha):

        norm = np.linalg.norm(Y, axis=0)
        projection = Y / np.maximum(1, norm / alpha)

        return projection

    def tgv2_denoising_gen(self, dataset_type, dataset_noisy, params, spac):

        self.h_inv = spac[0]
        self.hz_inv = spac[1]

        if dataset_type == ProcessSelDataType.SLICE_2D:
            temp = np.zeros((1, *dataset_noisy.shape))
            temp[0, :, :] = dataset_noisy
            dataset_noisy = temp

            dataset_denoised = self.tgv2_denoising(
                dataset_noisy, *params)[0, :, :]

            return dataset_denoised

        elif dataset_type == ProcessSelDataType.WHOLE_SCAN_2D:

            dataset_denoised = self.tgv2_denoising(dataset_noisy, *params)

            return dataset_denoised

        elif dataset_type == ProcessSelDataType.WHOLE_SCAN_3D:

            dataset_denoised = self.tgv2_denoising(dataset_noisy, *params)

            return dataset_denoised

        else:
            raise TypeError(
                "Dataset must be either 2D or 3D and matching the correct dataset type")

    @profile
    def tgv2_denoising(self, img_noisy, lambd, alpha0, alpha1, iterations):

        # Parameters
        beta = 1
        theta = 1
        mu = 0.5
        delta = 0.99

        # inverted spacing is used so that h* = 0 is an infinite spacing
        f = img_noisy

        L, M, N = f.shape
        img = img_noisy.reshape(L * M * N)

        # make operators
        k = self.make_K(L, M, N)

        # initialize primal variables
        u_old = np.zeros(L * M * N)
        v_old = np.zeros(3 * L * M * N)

        # initialize dual variables
        p_old = np.zeros(3 * L * M * N)
        q_old = np.zeros(9 * L * M * N)

        # primal and dual step size
        tau_old = self.tau_init
        sigma = self.tau_init

        x_vec_old = np.concatenate([u_old, v_old])
        y_vec_old = np.concatenate([p_old, q_old])

        for it in range(0, iterations):
            print("iterations: " + str(it))
            x_vec_new = x_vec_old - tau_old * k.T @ y_vec_old
            u_new = self.prox_G(x_vec_new[0:L * M * N], img, tau_old, lambd)
            v_new = x_vec_new[L * M * N:12 * L * M * N]
            x_vec_new = np.concatenate([u_new, v_new])

            tau_new = tau_old * (1 + theta)**0.5

            while True:
                theta = tau_new / tau_old
                sigma = beta * tau_new
                x_bar = x_vec_new + theta * (x_vec_new - x_vec_old)

                y_temp = y_vec_old + sigma * k @ (x_bar)
                p_new = np.ravel(self.proj_ball(
                    y_temp[0:3 * L * M * N].reshape(3, L * M * N), alpha1))
                q_new = np.ravel(self.proj_ball(
                    y_temp[3 * L * M * N:12 * L * M * N].reshape(9, L * M * N), alpha0))
                y_vec_new = np.concatenate([p_new, q_new])

                LS = np.sqrt(beta) * tau_new * \
                    (np.linalg.norm(k.T @ y_vec_new - k.T @ y_vec_old))
                RS = delta * (np.linalg.norm(y_vec_new - y_vec_old))

                if LS <= RS:
                    break
                else:
                    tau_new = tau_new * mu

            # update variables
            x_vec_old = x_vec_new
            y_vec_old = y_vec_new
            tau_old = tau_new

        u_new = u_new.reshape(L, M, N)
        return u_new

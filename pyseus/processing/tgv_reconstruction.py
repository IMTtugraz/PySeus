import numpy as np
import scipy
import scipy.sparse as sp

from ..settings import ProcessSelDataType


class TGV_Reco():

    def __init__(self):

        # inverted spacing is used so that h* = 0 is an infinite spacing
        self.h_inv = 1.0
        self.hz_inv = 1.0

        self.tau_init = 10

        self.fft_dim = (-2, -1)

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

    def proj_ball(self, Y, alpha):

        norm = np.linalg.norm(Y, axis=0)
        projection = Y / np.maximum(1, norm / alpha)

        return projection

    def prox_F(self, r, sigma, lambd):

        # this is from knoll stollberger tgv paper
        return (r * lambd) / (lambd + sigma)

    def op_A(self, u, sens_c, sparse_mask):

        return sparse_mask * \
            np.fft.fftn((sens_c * u), axes=self.fft_dim, norm='ortho')

    def op_A_conj(self, r, sens_c, sparse_mask):

        r_IFT = sens_c.conjugate() * np.fft.ifftn(r * sparse_mask,
                                                  axes=self.fft_dim, norm='ortho')

        return np.sum(r_IFT, axis=0)

    def tgv2_reconstruction_gen(
            self,
            dataset_type,
            data_raw,
            data_coils,
            params,
            spac):

        self.h_inv = spac[0]
        self.hz_inv = spac[1]

        sparse_mask = (data_raw != 0)

        if dataset_type == ProcessSelDataType.SLICE_2D:

            dataset_denoised = self.tgv2_reconstruction(
                data_raw, data_coils, sparse_mask, *params)[0, :, :]

            return dataset_denoised

        elif dataset_type == ProcessSelDataType.WHOLE_SCAN_2D:

            self.fft_dim = (-2, -1)

            dataset_denoised = self.tgv2_reconstruction(
                data_raw, data_coils, sparse_mask, *params)

            return dataset_denoised

        elif dataset_type == ProcessSelDataType.WHOLE_SCAN_3D:

            self.fft_dim = (-3, -2, -1)

            dataset_denoised = self.tgv2_reconstruction(
                data_raw, data_coils, sparse_mask, *params)

            return dataset_denoised

        else:
            raise TypeError(
                "Dataset must be either 2D or 3D and matching the correct dataset type")

    def tgv2_reconstruction(
            self,
            img_kspace,
            sens_coils,
            sparse_mask,
            lambd,
            alpha0,
            alpha1,
            iterations):

        # Parameters
        beta = 1
        theta = 1
        mu = 0.5
        delta = 0.99

        d = img_kspace / np.linalg.norm(img_kspace)

        C, L, M, N = d.shape

        # make operators
        k = self.make_K(L, M, N)

        # initialize primal variables - numpy arrays shape (L*M*N, )
        u_old = np.zeros(L * M * N, dtype=np.complex)
        v_old = np.zeros(3 * L * M * N, dtype=np.complex)

        # initialize dual variables
        p_old = np.zeros(3 * L * M * N, dtype=np.complex)
        q_old = np.zeros(9 * L * M * N, dtype=np.complex)
        r_old = np.zeros(C * L * M * N, dtype=np.complex)

        # primal and dual step size
        tau_old = self.tau_init
        sigma = self.tau_init

        x_old = np.concatenate([u_old, v_old])
        pq_old = np.concatenate([p_old, q_old])
        y_old = np.zeros((3 + 9 + C) * L * M * N, dtype=np.complex)
        kTy_old = np.zeros_like(x_old, dtype=np.complex)

        # temp vector for DAH*r
        Aconj_r = np.zeros_like(x_old, dtype=np.complex)

        for it in range(0, iterations):

            print("iterations: " + str(it))

            # add result of DAHr only to first L*M*N entries, because they
            # belong to the u_vec , v_vec should not be influenced
            Aconj_r[0:L * M * N] = np.ravel(self.op_A_conj(
                r_old.reshape(C, L, M, N), sens_coils, sparse_mask))

            # prox for u not necessary
            x_new = x_old - tau_old * (k.T @ pq_old + Aconj_r)

            tau_new = tau_old * (1 + theta)**0.5

            while True:
                theta = tau_new / tau_old
                sigma = beta * tau_new
                x_bar = x_new + theta * (x_new - x_old)

                pq_temp = pq_old + sigma * k @ (x_bar)
                p_new = np.ravel(self.proj_ball(
                    pq_temp[0:3 * L * M * N].reshape(3, L * M * N), alpha1))
                q_new = np.ravel(self.proj_ball(
                    pq_temp[3 * L * M * N:12 * L * M * N].reshape(9, L * M * N), alpha0))
                pq_new = np.concatenate([p_new, q_new])
                r_temp = r_old + \
                    np.ravel(sigma * (self.op_A(x_bar[0:L * M * N].reshape(L, M, N), sens_coils, sparse_mask) - d))
                r_new = np.ravel(self.prox_F(r_temp, sigma, lambd))

                Aconj_r[0:L * M * N] = np.ravel(self.op_A_conj(
                    r_new.reshape(C, L, M, N), sens_coils, sparse_mask))
                kTy_new = k.T @ pq_new + Aconj_r
                y_new = np.concatenate([pq_new, r_new])

                LS = np.sqrt(beta) * tau_new * \
                    (np.linalg.norm(kTy_new - kTy_old))
                RS = delta * (np.linalg.norm(y_new - y_old))

                if LS <= RS:
                    break
                else:
                    tau_new = tau_new * mu

            # update variables
            x_old = x_new
            pq_old = pq_new
            r_old = r_new
            y_old = y_new
            kTy_old = kTy_new
            tau_old = tau_new

        u_new = x_new[0:L * M * N].reshape(L, M, N)

        return u_new

import numpy as np
import scipy
import scipy.sparse as sp

from ..settings import ProcessSelDataType

from memory_profiler import profile


class TV_Reco():

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

        K = sp.bmat([[nabla_x], [nabla_y], [nabla_z]])

        return K

    def proj_ball(self, Y):

        norm = np.linalg.norm(Y, axis=0)
        projection = Y / np.maximum(1, norm)

        return projection

    def prox_F(self, r, sigma, lambd):

        return (r * lambd) / (lambd + sigma)

    def op_A(self, u, sens_c, sparse_mask):

        return sparse_mask * \
            np.fft.fftn((sens_c * u), axes=self.fft_dim, norm='ortho')

    def op_A_conj(self, r, sens_c, sparse_mask):

        r_IFT = sens_c.conjugate() * np.fft.ifftn(r * sparse_mask,
                                                  axes=self.fft_dim, norm='ortho')

        return np.sum(r_IFT, axis=0)

    def tv_reconstruction_gen(
            self,
            func_reco,
            dataset_type,
            data_raw,
            data_coils,
            params,
            spac):

        self.h_inv = spac[0]
        self.hz_inv = spac[1]

        sparse_mask = (data_raw != 0)

        if dataset_type == ProcessSelDataType.SLICE_2D:

            dataset_denoised = func_reco(
                data_raw,
                data_coils,
                sparse_mask,
                *
                params)[
                0,
                :,
                :]

            return dataset_denoised

        elif dataset_type == ProcessSelDataType.WHOLE_SCAN_2D:

            self.fft_dim = (-2, -1)

            dataset_denoised = func_reco(
                data_raw, data_coils, sparse_mask, *params)

            return dataset_denoised

        elif dataset_type == ProcessSelDataType.WHOLE_SCAN_3D:

            self.fft_dim = (-3, -2, -1)

            dataset_denoised = func_reco(
                data_raw, data_coils, sparse_mask, *params)

            return dataset_denoised

        else:
            raise TypeError(
                "Dataset must be either 2D or 3D and matching the correct dataset type")

    @profile
    def tv_l2_reconstruction(
            self,
            img_kspace,
            sens_coils,
            sparse_mask,
            lambd,
            iterations):

        # Parameters
        beta = 1
        theta = 1
        mu = 0.5
        delta = 0.99

        d = img_kspace

        C, L, M, N = d.shape

        # make operators
        k = self.make_K(L, M, N)

        # this is basically u_old, just defined here for better readability
        u_old = np.zeros(L * M * N, dtype=np.complex)

        # initialize dual variables
        p_old = np.zeros(3 * L * M * N, dtype=np.complex)
        r_old = np.zeros(C * L * M * N, dtype=np.complex)

        # primal and dual step size
        tau_old = self.tau_init
        sigma = self.tau_init

        y_old = np.zeros((3 + C) * L * M * N, dtype=np.complex)
        kTy_old = np.zeros_like(u_old, dtype=np.complex)

        # temp vector for A* * r
        Aconj_r = np.zeros_like(u_old, dtype=np.complex)

        for it in range(0, iterations):
            print("iterations: " + str(it))

            # add result of DAHr only to first L*M*N entries, because they
            # belong to the u_vec , v_vec should not be influenced
            Aconj_r = np.ravel(
                self.op_A_conj(
                    r_old.reshape(
                        C,
                        L,
                        M,
                        N),
                    sens_coils,
                    sparse_mask))

            u_new = u_old - tau_old * (k.T @ p_old + Aconj_r)

            tau_new = tau_old * (1 + theta)**0.5

            while True:
                theta = tau_new / tau_old
                sigma = beta * tau_new
                u_bar = u_new + theta * (u_new - u_old)

                p_temp = p_old + sigma * k @ (u_bar)
                p_new = np.ravel(self.proj_ball(p_temp.reshape(3, L * M * N)))
                r_temp = r_old + \
                    np.ravel(sigma * (self.op_A(u_bar.reshape(L, M, N), sens_coils, sparse_mask) - d))
                r_new = np.ravel(self.prox_F(r_temp, sigma, lambd))

                Aconj_r = np.ravel(
                    self.op_A_conj(
                        r_new.reshape(
                            C,
                            L,
                            M,
                            N),
                        sens_coils,
                        sparse_mask))
                kTy_new = k.T @ p_new + Aconj_r
                y_new = np.concatenate([p_new, r_new])

                LS = np.sqrt(beta) * tau_new * \
                    (np.linalg.norm(kTy_new - kTy_old))
                RS = delta * (np.linalg.norm(y_new - y_old))

                if LS <= RS:
                    break
                else:
                    tau_new = tau_new * mu

            # update variables
            u_old = u_new
            p_old = p_new
            r_old = r_new
            y_old = y_new
            kTy_old = kTy_new
            tau_old = tau_new

        u_new = u_new.reshape(L, M, N)

        return u_new

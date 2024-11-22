import numpy as np
import matplotlib.pyplot as plt

class ACOBridge:
    """
    An Class that Represent ACO in two bridge
    """
    def __init__(self, alpha:float = 1, ratio:int = 2, t:int = 100, n_ants:int = 10) -> None:
        """
        Initialise Parameter to run ACO
        
        :param alpha: (float) Rate dari semut meninggalkan jejak pada sebuah path
        :param ratio: (int) Perbedaan panjang antara Short dan Long path
        :param t: (int) Jumlah iterasi atau jumlah waktu yang akan dihabiskan semut selama loop
        :param n_ants: (int) Jumlah semut
        """
        self.alpha = alpha
        self.path = [1, 1*ratio]
        self.times = t
        self.n_ants = n_ants
        self.phi = [0.5, 0.5]
        self.ant_histories = []
        self.choice_histories = []
    
    def compute_probabilities(self):
        p_is = (self.phi[0]**self.alpha) / ((self.phi[0]**self.alpha) + (self.phi[1]**self.alpha))
        p_il = (self.phi[1]**self.alpha) / ((self.phi[0]**self.alpha) + (self.phi[1]**self.alpha))
        self.choice_histories.append((p_is,p_il))
        return p_is, p_il
    
    def pheromone_update(self, short_ants, long_ants):
        phi_is = self.phi[0] + short_ants * (1 / self.path[0])
        phi_il = self.phi[1] + long_ants * (1 / self.path[1])
        self.phi[0], self.phi[1] = phi_is, phi_il
        return phi_is, phi_il

    def run(self):
        for iteration in range(self.times):
            p_is, p_il = self.compute_probabilities()
            
            ant_choices = np.random.choice([0, 1], size=self.n_ants, p=[p_is, p_il])
            short_ants = np.sum(ant_choices == 0) 
            long_ants = np.sum(ant_choices == 1) 
            
            self.ant_histories.append((short_ants, long_ants))
            
            self.pheromone_update(short_ants, long_ants)

            if abs(p_is - 1) < 1e-3:
                break
    
    def show_plots(self):
        fig, axs = plt.subplots(1, 2, figsize=(10, 12))
        
        short_counts = [ _[0] for _ in self.ant_histories]
        long_counts = [ _[1] for _ in self.ant_histories]
        axs[0].plot(short_counts, label="Semut pada jalur pendek (Short)")
        axs[0].plot(long_counts, label="Semut pada jalur panjang (Long)")
        axs[0].set(xlabel="t steps", ylabel="Jumlah Semut", title="Jumlah Semut yang Melewati Jalur Pendek dan Panjang")
        axs[0].legend()
        axs[0].grid(True)
        
        p_is_hist = [ _[0] for _ in self.choice_histories]
        p_il_hist = [ _[1] for _ in self.choice_histories]
        axs[1].plot(p_is_hist, label="Probability Short path")
        axs[1].plot(p_il_hist, label="Probability Long path")
        axs[1].set(xlabel="t steps", ylabel="Choice Probabilities", title="Sebaran Probabilitas berdasarkan iterasi")
        axs[1].legend()
        axs[1].grid(True)
        
        plt.tight_layout()
        plt.show()
        


if __name__ == "__main__":
    aco = ACOBridge(alpha=2, ratio=3, n_ants=100)
    aco.run()
    aco.show_plots()

import matplotlib.pyplot as plt
import json
import os 
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

result_path = "/home/jeongjw/selective-code-generation/result/exp/exp_model"
output_path = "/home/jeongjw/selective-code-generation/result/plot/exp_model"
exp_lst = ['SCG-EM', 'SCG-small', 'SCG-manual', 'SCG-H', 'SCG']
# exp_lst = ['SCG-small', 'SCG-manual', 'SCG-H', 'SCG']

width = 0.4
codellama_alpha = 0.35
alpha = 0.35
del_s = 0.1
eps_s = 0.3
eps_e = 0.05
eps_eval = 0.01
calib_lim = 50
eval_lim = 150

def plot(
    model_type: str,
    dataset_type: str,
    alpha: float,
    del_s: float,
    eps_s: float,
    eps_e: float,
    eps_eval: float,
    calib_lim: int,
    eval_lim: int,
    add_eps: bool,
    ax1_ylim_min: float,
    ax1_ylim_max: float,
    ax2_ylim_min: float,
    ax2_ylim_max: float
):
    original_calib_lim = calib_lim

    fdr_lst_lst = []
    eff_lst_lst = []
    

    # read exp file 
    for exp in exp_lst:

        if exp == 'SCG-EM' or exp == 'SCG-H':
            add_eps = False
        else:
            add_eps = True

        
        if exp == 'SCG-small':
            calib_lim = 21
        else:
            calib_lim = original_calib_lim

        result_file_name = f'result_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}_add_eps_{add_eps}.json'
        result_file_path = os.path.join(result_path, exp,result_file_name)
        print(result_file_path)

        with open(result_file_path, 'r') as f:
            result = json.load(f)

        exp_fdr = result['fdr']
        exp_eff = result['eff']

        fdr_lst_lst.append(exp_fdr)
        eff_lst_lst.append(exp_eff)

        print(f'mean: {np.mean(exp_fdr)} std: {np.std(exp_fdr)}')
        print(exp_fdr[0])

    
    # draw plot
    plot_file_name = f'plot_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}.pdf'
    plot_file_path = os.path.join(output_path, plot_file_name)


    with PdfPages(plot_file_path) as pdf:

        # basic var
        positions = [1, 2, 3, 4, 5]
        # positions = [1, 2, 3, 4]
        whis = (del_s * 100, (1-del_s)*100)


        # basic setup
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        fdr_boxes = []
        eff_boxes = []


        # draw FDR box plots
        for i in range(len(positions)):
            box1 = ax1.boxplot(
                fdr_lst_lst[i], positions=[positions[i] - width/2], widths=width, patch_artist=True, whis=whis,
                boxprops=dict(facecolor=(1, 0.5, 0, 0), color='black', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.25),
                capprops=dict(color='black', linewidth=1.25),
                medianprops=dict(color='black', linewidth=1),
                labels=['FDR'],
                flierprops=dict(marker='o', color='red', alpha=0.6, markersize=2),
            )
            fdr_boxes.append(box1["boxes"][0])

        
        # axis 1 ylabel
        ax1.set_ylim(ax1_ylim_min, ax1_ylim_max)
        epsilon_line = ax1.axhline(y=eps_s, color='k', linestyle='dashed', zorder=4)


        # draw efficiency box plots
        for i in range(len(positions)):
            box2 = ax2.boxplot(
                eff_lst_lst[i], positions=[positions[i] + width/2], widths=width, patch_artist=True, whis=whis,
                boxprops=dict(facecolor=(1, 0.5, 0, 0), color='orange', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.25),
                capprops=dict(color='black', linewidth=1.25),
                medianprops=dict(color='black', linewidth=1),
                labels=['Efficiency'],
                flierprops=dict(marker='o', color='red', alpha=0.6, markersize=2),
            )
            eff_boxes.append(box2["boxes"][0]) 

        
        # axis 2 ylabel
        ax2.set_ylabel('Effciency')
        ax2.set_ylim(ax2_ylim_min, ax2_ylim_max)

        
        # axis1 legened
        ax1.legend(
            handles=[fdr_boxes[0], eff_boxes[0], epsilon_line], 
            labels=['FDR', 'Efficiency', f'$\epsilon_S = {eps_s}$'],
            loc='upper right'
        )
        ax1.set_xticks(positions, exp_lst)
        ax1.set_ylabel('FDR-CE')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        plt.show()
        pdf.savefig(bbox_inches='tight')


if __name__ == "__main__":
    os.makedirs(output_path, exist_ok=True)
    plot(
        model_type="gpt-4o",
        dataset_type="APPS",
        alpha=alpha,
        del_s=del_s,
        eps_s=eps_s,
        eps_e=eps_e,
        eps_eval=eps_eval,
        calib_lim=calib_lim,
        eval_lim=eval_lim,
        add_eps=False,
        ax1_ylim_min=0.0,
        ax1_ylim_max=1.0,
        ax2_ylim_min=0.0,
        ax2_ylim_max=0.6
    )

    plot(
        model_type="gemini",
        dataset_type="APPS",
        alpha=alpha,
        del_s=del_s,
        eps_s=eps_s,
        eps_e=eps_e,
        eps_eval=eps_eval,
        calib_lim=calib_lim,
        eval_lim=eval_lim,
        add_eps=False,
        ax1_ylim_min=0.00,
        ax1_ylim_max=0.6,
        ax2_ylim_min=0.00,
        ax2_ylim_max=0.6
    )

    plot(
        model_type="codellama-13b-instruct",
        dataset_type="APPS",
        alpha=codellama_alpha,
        del_s=del_s,
        eps_s=eps_s,
        eps_e=eps_e,
        eps_eval=eps_eval,
        calib_lim=calib_lim,
        eval_lim=eval_lim,
        add_eps=False,
        ax1_ylim_min=0.0,
        ax1_ylim_max=1.0,
        ax2_ylim_min=0.0,
        ax2_ylim_max=1.0
    )

    plot(
        model_type="deepseek-r1",
        dataset_type="APPS",
        alpha=alpha,
        del_s=del_s,
        eps_s=eps_s,
        eps_e=eps_e,
        eps_eval=eps_eval,
        calib_lim=calib_lim,
        eval_lim=eval_lim,
        add_eps=False,
        ax1_ylim_min=0.00,
        ax1_ylim_max=1.0,
        ax2_ylim_min=0.0,
        ax2_ylim_max=1.0
    )

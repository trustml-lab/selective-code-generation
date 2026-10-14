import matplotlib.pyplot as plt
import json
import os 
from matplotlib.backends.backend_pdf import PdfPages
from typing import List

result_path = "/home/jeongjw/selective-code-generation/result/exp/exp_parameter"
output_path = "/home/jeongjw/selective-code-generation/result/plot/exp_parameter"
# exp_lst = ['SCG-small', 'SCG-manual', 'SCG-H', 'SCG']

width = 0.4
default_alpha = 0.35
default_epsilon_s = 0.3
default_delta_s = 0.1
default_epsilon_e = 0.05
default_epsilon_eval = 0.01
default_calib_lim = 50
default_eval_lim = 100
default_add_eps = False


def plot_varying_epsilon_s(
    model_type: str,
    dataset_type: str,
    alpha: float,
    del_s: float,
    eps_s_lst: List[float],
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

    fdr_lst_lst = []
    eff_lst_lst = []

    for eps_s in eps_s_lst:
        result_file_name = f'result_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}_add_eps_{add_eps}.json'
        result_file_path = os.path.join(result_path, "epsilon_s", result_file_name)

        with open(result_file_path, 'r') as f:
            result = json.load(f)

        exp_fdr = result['fdr']
        exp_eff = result['eff']

        fdr_lst_lst.append(exp_fdr)
        eff_lst_lst.append(exp_eff)
    
    plot_file_name = f'plot_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_varying_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}.pdf'
    plot_file_path = os.path.join(output_path, plot_file_name)

    with PdfPages(plot_file_path) as pdf:
        positions = [1, 2, 3, 4]

        whis = (del_s * 100, (1-del_s)*100)

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        fdr_boxes = []
        eff_boxes = []

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
            eff_boxes.append(box2['boxes'][0])

        ax1.set_ylim(ax1_ylim_min, ax1_ylim_max)
        ax1.set_ylabel('FDR-CE')
        ax1.set_xlim(positions[0] - 0.5,  positions[-1] + 0.5)
        ax1.set_xlabel('$\\epsilon_S$')

        ax1.set_xticks(positions, eps_s_lst)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(
            handles=[fdr_boxes[0], eff_boxes[0]], 
            labels=['FDR-CE', 'Efficiency'],
            loc='upper left'
        )


        normalize_factor = 2*(positions[-1] - positions[0] + 1)
        for i in range(len(positions)):
            ax1.axhline(y=eps_s_lst[i], xmin=(2*i + 1)/normalize_factor-0.1125, xmax=(2*i + 1)/normalize_factor+0.01, color='k', linestyle='dashed', zorder=4)


        ax2.set_ylim(ax2_ylim_min, ax2_ylim_max)
        ax2.set_ylabel('Efficiency')

        pdf.savefig(bbox_inches='tight')


def plot_varying_delta_s(
    model_type: str,
    dataset_type: str,
    alpha: float,
    del_s_lst: List[float],
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
    fdr_lst_lst = []
    eff_lst_lst = []

    for del_s in del_s_lst:
        result_file_name = f'result_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}_add_eps_{add_eps}.json'
        result_file_path = os.path.join(result_path, "delta_s", result_file_name)

        with open(result_file_path, 'r') as f:
            result = json.load(f)

        exp_fdr = result['fdr']
        exp_eff = result['eff']

        fdr_lst_lst.append(exp_fdr)
        eff_lst_lst.append(exp_eff)
    
    plot_file_name = f'plot_{model_type}_{dataset_type}_alpha_{alpha}_del_s_varying_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}.pdf'
    plot_file_path = os.path.join(output_path, plot_file_name)

    with PdfPages(plot_file_path) as pdf:
        positions = [1, 2, 3]

        whis = [(100 * ele, 100 * (1 - ele)) for ele in del_s_lst]

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        fdr_boxes = []
        eff_boxes = []

        for i in range(len(positions)):
            box1 = ax1.boxplot(
                fdr_lst_lst[i], positions=[positions[i] - width/2], widths=width, patch_artist=True, whis=whis[i],
                boxprops=dict(facecolor=(1, 0.5, 0, 0), color='black', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.25),
                capprops=dict(color='black', linewidth=1.25),
                medianprops=dict(color='black', linewidth=1),
                labels=['FDR'],
                flierprops=dict(marker='o', color='red', alpha=0.6, markersize=2),
            )
            fdr_boxes.append(box1["boxes"][0])

        for i in range(len(positions)):
            box2 = ax2.boxplot(
                eff_lst_lst[i], positions=[positions[i] + width/2], widths=width, patch_artist=True, whis=whis[i],
                boxprops=dict(facecolor=(1, 0.5, 0, 0), color='orange', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.25),
                capprops=dict(color='black', linewidth=1.25),
                medianprops=dict(color='black', linewidth=1),
                labels=['Efficiency'],
                flierprops=dict(marker='o', color='red', alpha=0.6, markersize=2),
            )
            eff_boxes.append(box2['boxes'][0])

        ax1.set_ylim(ax1_ylim_min, ax1_ylim_max)
        ax1.set_ylabel('FDR-CE')
        ax1.set_xlim(positions[0] - 0.5,  positions[-1] + 0.5)
        ax1.set_xlabel('$\\delta_S$')

        ax1.set_xticks(positions, del_s_lst)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(
            handles=[fdr_boxes[0], eff_boxes[0]], 
            labels=['FDR-CE', 'Efficiency'],
            loc='upper left'
        )


        normalize_factor = 2*(positions[-1] - positions[0] + 1)
        ax1.axhline(y=eps_s, color='k', linestyle='dashed', zorder=4)


        ax2.set_ylim(ax2_ylim_min, ax2_ylim_max)
        ax2.set_ylabel('Efficiency')

        pdf.savefig(bbox_inches='tight')


def plot_varying_epsilon_e(
    model_type: str,
    dataset_type: str,
    alpha: float,
    del_s: float,
    eps_s: float,
    eps_e_lst: List[float],
    eps_eval: float,
    calib_lim: int,
    eval_lim: int,
    add_eps: bool,
    ax1_ylim_min: float,
    ax1_ylim_max: float,
    ax2_ylim_min: float,
    ax2_ylim_max: float
):
    fdr_lst_lst = []
    eff_lst_lst = []

    for eps_e in eps_e_lst:
        result_file_name = f'result_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}_add_eps_{add_eps}.json'
        result_file_path = os.path.join(result_path, "epsilon_e", result_file_name)

        with open(result_file_path, 'r') as f:
            result = json.load(f)

        exp_fdr = result['fdr']
        exp_eff = result['eff']

        fdr_lst_lst.append(exp_fdr)
        eff_lst_lst.append(exp_eff)
    
    plot_file_name = f'plot_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_varying_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}.pdf'
    plot_file_path = os.path.join(output_path, plot_file_name)

    with PdfPages(plot_file_path) as pdf:
        positions = [1, 2, 3, 4]

        whis = (100*del_s, 100*(1-del_s))

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        fdr_boxes = []
        eff_boxes = []

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
            eff_boxes.append(box2['boxes'][0])

        ax1.set_ylim(ax1_ylim_min, ax1_ylim_max)
        ax1.set_ylabel('FDR-CE')
        ax1.set_xlim(positions[0] - 0.5,  positions[-1] + 0.5)
        ax1.set_xlabel('$\\epsilon_E$')

        ax1.set_xticks(positions, eps_e_lst)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(
            handles=[fdr_boxes[0], eff_boxes[0]], 
            labels=['FDR-CE', 'Efficiency'],
            loc='upper left'
        )


        normalize_factor = 2*(positions[-1] - positions[0] + 1)
        ax1.axhline(y=eps_s, color='k', linestyle='dashed', zorder=4)


        ax2.set_ylim(ax2_ylim_min, ax2_ylim_max)
        ax2.set_ylabel('Efficiency')

        pdf.savefig(bbox_inches='tight')


def plot_varying_alpha(
    model_type: str,
    dataset_type: str,
    alpha_lst: List[float],
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
    fdr_lst_lst = []
    eff_lst_lst = []

    for alpha in alpha_lst:
        result_file_name = f'result_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}_add_eps_{add_eps}.json'
        result_file_path = os.path.join(result_path, "alpha", result_file_name)

        with open(result_file_path, 'r') as f:
            result = json.load(f)

        exp_fdr = result['fdr']
        exp_eff = result['eff']

        fdr_lst_lst.append(exp_fdr)
        eff_lst_lst.append(exp_eff)
    
    plot_file_name = f'plot_{model_type}_{dataset_type}_alpha_varying_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}.pdf'
    plot_file_path = os.path.join(output_path, plot_file_name)

    with PdfPages(plot_file_path) as pdf:
        positions = [1, 2, 3, 4, 5]

        whis = (100*del_s, 100*(1-del_s))

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        fdr_boxes = []
        eff_boxes = []

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
            eff_boxes.append(box2['boxes'][0])

        ax1.set_ylim(ax1_ylim_min, ax1_ylim_max)
        ax1.set_ylabel('FDR-CE')
        ax1.set_xlim(positions[0] - 0.5,  positions[-1] + 0.5)
        ax1.set_xlabel('$\\alpha$')

        ax1.set_xticks(positions, alpha_lst)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(
            handles=[fdr_boxes[0], eff_boxes[0]], 
            labels=['FDR-CE', 'Efficiency'],
            loc='upper left'
        )


        normalize_factor = 2*(positions[-1] - positions[0] + 1)
        ax1.axhline(y=eps_s, color='k', linestyle='dashed', zorder=4)


        ax2.set_ylim(ax2_ylim_min, ax2_ylim_max)
        ax2.set_ylabel('Efficiency')

        pdf.savefig(bbox_inches='tight')


def plot_varying_eval_limit(
    model_type: str,
    dataset_type: str,
    alpha: float,
    del_s: float,
    eps_s: float,
    eps_e: float,
    eps_eval: float,
    calib_lim: int,
    eval_lim_lst: List[int],
    add_eps: bool,
    ax1_ylim_min: float,
    ax1_ylim_max: float,
    ax2_ylim_min: float,
    ax2_ylim_max: float
):
    fdr_lst_lst = []
    eff_lst_lst = []

    for eval_lim in eval_lim_lst:
        result_file_name = f'result_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_{eval_lim}_add_eps_{add_eps}.json'
        result_file_path = os.path.join(result_path, "eval_limit", result_file_name)

        with open(result_file_path, 'r') as f:
            result = json.load(f)

        exp_fdr = result['fdr']
        exp_eff = result['eff']

        fdr_lst_lst.append(exp_fdr)
        eff_lst_lst.append(exp_eff)
    
    plot_file_name = f'plot_{model_type}_{dataset_type}_alpha_{alpha}_del_s_{del_s}_eps_s_{eps_s}_eps_e_{eps_e}_eps_eval_{eps_eval}_calib_lim_{calib_lim}_eval_lim_varying.pdf'
    plot_file_path = os.path.join(output_path, plot_file_name)

    with PdfPages(plot_file_path) as pdf:
        positions = [1, 2, 3, 4]

        whis = (100*del_s, 100*(1-del_s))

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        fdr_boxes = []
        eff_boxes = []

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
            eff_boxes.append(box2['boxes'][0])

        ax1.set_ylim(ax1_ylim_min, ax1_ylim_max)
        ax1.set_ylabel('FDR-CE')
        ax1.set_xlim(positions[0] - 0.5,  positions[-1] + 0.5)
        ax1.set_xlabel('Number of unit tests for evaluation')

        ax1.set_xticks(positions, eval_lim_lst)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(
            handles=[fdr_boxes[0], eff_boxes[0]], 
            labels=['FDR-CE', 'Efficiency'],
            loc='upper left'
        )


        normalize_factor = 2*(positions[-1] - positions[0] + 1)
        ax1.axhline(y=eps_s, color='k', linestyle='dashed', zorder=4)


        ax2.set_ylim(ax2_ylim_min, ax2_ylim_max)
        ax2.set_ylabel('Efficiency')

        pdf.savefig(bbox_inches='tight')


if __name__ == "__main__":
    os.makedirs(output_path, exist_ok=True)
    plot_varying_epsilon_s(
        model_type="gpt-4o",
        dataset_type="APPS",
        alpha=0.35,
        del_s=0.1,
        eps_s_lst=[0.2, 0.3, 0.4, 0.5],
        eps_e=0.05,
        eps_eval=0.01,
        calib_lim=100,
        eval_lim=150,
        add_eps=True,
        ax1_ylim_min=0.0,
        ax1_ylim_max=0.55,
        ax2_ylim_min=0.05,
        ax2_ylim_max=1.0
    )

    plot_varying_delta_s(
        model_type="gpt-4o",
        dataset_type="APPS",
        alpha=0.35,
        del_s_lst=[0.001, 0.01, 0.1],
        eps_s=0.3,
        eps_e=0.05,
        eps_eval=0.01,
        calib_lim=100,
        eval_lim=150,
        add_eps=True,
        ax1_ylim_min=0.05,
        ax1_ylim_max=0.35,
        ax2_ylim_min=0.2,
        ax2_ylim_max=0.45
    )

    plot_varying_epsilon_e(
        model_type="gpt-4o",
        dataset_type="APPS",
        alpha=0.35,
        del_s=0.1,
        eps_s=0.3,
        eps_e_lst=[0.05, 0.1, 0.15, 0.2],
        eps_eval=0.01,
        calib_lim=100,
        eval_lim=150,
        add_eps=True,
        ax1_ylim_min=0.00,
        ax1_ylim_max=0.35,
        ax2_ylim_min=0.00,
        ax2_ylim_max=0.45
    )

    plot_varying_alpha(
        model_type="gpt-4o",
        dataset_type="APPS",
        alpha_lst=[0.1, 0.2, 0.3, 0.4, 0.5],
        del_s=0.1,
        eps_s=0.3,
        eps_e=0.05,
        eps_eval=0.01,
        calib_lim=100,
        eval_lim=150,
        add_eps=True,
        ax1_ylim_min=0.15,
        ax1_ylim_max=0.35,
        ax2_ylim_min=0.2,
        ax2_ylim_max=0.45
    )

    plot_varying_eval_limit(
        model_type="gpt-4o",
        dataset_type="APPS",
        alpha=0.35,
        del_s=0.1,
        eps_s=0.3,
        eps_e=0.05,
        eps_eval=0.01,
        calib_lim=50,
        eval_lim_lst=[25, 70, 110, 150],
        add_eps=True,
        ax1_ylim_min=0.15,
        ax1_ylim_max=0.35,
        ax2_ylim_min=0.2,
        ax2_ylim_max=0.45
    )

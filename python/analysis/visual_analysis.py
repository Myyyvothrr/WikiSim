import sys
sys.path.extend(['../../', '../', './'])

from similaritymeasures.deltacon import *
import numpy as np
import matplotlib.pyplot as plt
import csv

def visualize(similarity_file, out_root, type, dataset=None, show=True, matplotlib=True, handle_nan=None):
    similarity_folder = os.path.join(out_root, type)
    if dataset is not None:
        folders = filter(lambda x: x.endswith(dataset), os.listdir(similarity_folder))
    else:
        folders = os.listdir(similarity_folder)

    # collect all similarities
    l1 = list()
    l2 = list()
    similarity = list()
    kernel = list()
    missing_files = 0
    for folder in folders:
        try:
            data = csv.DictReader(open(os.path.join(similarity_folder, folder, similarity_file)), skipinitialspace=True)

            for x in data:
                l1.append(x['Language1'])
                l2.append(x['Language2'])
                similarity.append(float(x['SimilarityScore']))
                try:
                    kernel.append(float(x['Kernel']))
                except KeyError:
                    # some tables may contain a Kernel column. if so, we read it here and plot it below
                    pass
        except FileNotFoundError:
            missing_files += 1

        def plot_it(sim, addendum=''):
            languages = np.unique(l1)
            np.sort(languages)
            n_lang = languages.shape[0]
            sim_matrix = np.nan * np.zeros([n_lang, n_lang])

            #ugly
            lang_dict = {languages[i]: i for i in range(n_lang)}
            for i in range(len(l1)):
                sim_matrix[lang_dict[l1[i]], lang_dict[l2[i]]] = sim[i]
                sim_matrix[lang_dict[l2[i]], lang_dict[l1[i]]] = sim[i]

            # print similarity matrix
            with open(os.path.join(similarity_folder, folder, folder + '_' + similarity_file[:-4] + addendum + '.matrix'), 'w') as f:
                # header
                f.write('\t'.join(languages) + '\n')

                if handle_nan is not None:
                    sim_matrix[np.isnan(sim_matrix)] = handle_nan

                # # normalization: (does not work if there is one or more NaNs present)
                # maxabs = np.max(np.abs(sim_matrix))
                # if maxabs <= 1.0:
                #     maxabs = 1.0 # if similarities are normalized, don't stretch them

                # the lines
                for i, l in enumerate(languages):
                    # f.write(l + '\t' + '\t'.join([str(x / maxabs) for x in sim_matrix[i,:]]) + '\n')
                    f.write(l + '\t' + '\t'.join([str(x) for x in sim_matrix[i,:]]) + '\n')


            if (matplotlib):
                fig, ax = plt.subplots()
                im = ax.imshow(sim_matrix) #, norm=matplotlib.colors.Normalize(vmin=0.001, vmax=0.1, clip=False))

                # We want to show all ticks...
                ax.set_xticks(np.arange(len(languages)))
                ax.set_yticks(np.arange(len(languages)))
                # ... and label them with the respective list entries
                ax.set_xticklabels(languages)
                ax.set_yticklabels(languages)

                # Rotate the tick labels and set their alignment.
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                         rotation_mode="anchor")

                # Loop over data dimensions and create text annotations.
                for i in range(len(languages)):
                    for j in range(len(languages)):
                        text = ax.text(j, i, f'{sim_matrix[i, j]:.2f}',
                                       ha="center", va="center", color="w", fontsize='xx-small')

                ax.set_title(f'{similarity_file[:-4]}\n of Wikipedia Topic \n{folder[:-3]} ({similarity_folder.split(os.path.sep)[-1]})')
                fig.tight_layout()
                plt.savefig(os.path.join(similarity_folder, folder, folder + '_' + similarity_file[:-4] + addendum + '.png'))
                if show:
                    plt.show()
                plt.close()

        plot_it(similarity)
        if len(kernel) > 0:
            plot_it(kernel, '_Kernel')


process_all = True
# similarity_root = os.path.join('/', 'home', 'pascal', 'Documents', 'Uni_synced', 'frankfurt', 'experimental_results', 'WikiSimNew', 'outputComplete', 'oecdTopics')
# similarity_root = os.path.join('/', 'home', 'pascal', 'Documents', 'Uni_synced', 'frankfurt', 'experimental_results', 'WikiSimNew', 'outputComplete', 'oecd')
# similarity_root = os.path.join('/', 'home', 'pascal', 'Documents', 'Uni_synced', 'frankfurt', 'experimental_results', 'WikiSimNew', 'output')
similarity_root = os.path.join('/', 'home', 'pascal', 'Documents', 'Uni_synced', 'frankfurt', 'experimental_results', 'WikiSimNew', 'graphsReduced')

similarity_files = ['deltaCON_intersection_personalized_rw_affinities_lowmem.csv',
                    'deltaCON_intersection_shortest_path_affinities.csv',
                    'deltaCON_personalized_rw_affinities.csv',
                    'deltaCON_shortest_path_affinities.csv',
                    'otherSim_ged_similarity.csv',
                    'otherSim_intersection_edge_jaccard_similarity.csv',
                    'otherSim_intersection_ged_similarity.csv',
                    'otherSim_intersection_rw_kernel.csv',
                    'otherSim_intersection_rw_kernel_10iter.csv',
                    # 'otherSim_intersection_rw_kernel_unnormalized.csv',
                    'otherSim_intersection_vertex_jaccard_similarity.csv',
                    'otherSim_vertex_edge_jaccard_similarity.csv',
                    'otherSim_vertex_jaccard_similarity.csv',]

replace_nan_with_value = -1.0

if __name__ == '__main__':
    if process_all:
        for similarity_file in similarity_files:
            print('Processing', similarity_file)
            try:
                visualize(similarity_file=similarity_file, out_root=similarity_root, type='gml', dataset=None, show=False, matplotlib=False, handle_nan=replace_nan_with_value)
            except IOError:
                pass
            except Exception as e:
                print(e)
            try:
                visualize(similarity_file=similarity_file, out_root=similarity_root, type='fullgml', dataset=None, show=False, matplotlib=False, handle_nan=replace_nan_with_value)
            except IOError:
                pass
            except Exception as e:
                print(e)

    else:

        # similarity_file = 'deltaCON_personalized_rw_affinities.csv'
        similarity_file = 'deltaCON_intersection_personalized_rw_affinities.csv'
        # similarity_file = 'deltaCON_shortest_path_affinities.csv'
        # similarity_file = 'otherSim_ged_similarity.csv'
        # similarity_file = 'otherSim_vertex_edge_jaccard_similarity.csv'
        # similarity_file = 'otherSim_vertex_jaccard_similarity.csv'

        #  for root in ['gml', 'fullgml']:
        root = 'gml'
        # use 'GML' for all datasets
        dataset = 'holydayGML'
        out_folder = os.path.join('..', '..', 'output', root)

        visualize(similarity_file=similarity_file, out_folder=out_folder, dataset=dataset)






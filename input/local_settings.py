"""
local settings, include settings from C++ code and fast transitions
"""
from collections import OrderedDict


def get_local_settings():
    """
    local settings for C++ codes
    """
    setting = {
        "system": {
            "condition": "cv",
            "initializer": "dlsode"
        },
        "network": {
            "merge_chatterings": "yes",
            "condense_chatterings": "yes",
            "not_allowed_out_species": [10],
            "spe_branching": 'false',
            "terminal_sp": 'false'
        },
        "propagator": {
            "primary_type": "from_file",
            "type": "dlsode",
            "sub_type": "time_propagator_cv_s2m_pgt",
            "convert_molar_concentration_to_mole_fraction": "no",
            "normalize_initial_concentration": "yes"
        },
        # trajectory max time, used to solve referene trajectory
        "traj_max_t": 0.779074999626780951,
        # trajectory critical time, after which print out more data points
        "traj_critical_t": 0.751999999880706205,
        # reference time, to a combustion system, this is gonna be the ignition delay time
        # for Propane, time when temperature=1800K
        # "tau": 0.777655955130997,
        # time at which the first order differential/gradient of temperature is maximized
        # check routine get_time_at_time_differential_maximum from trajectory.py
        "tau": 0.777660157519,
        # time at which using MC to generate pathway list, time=mc_t*tau
        # "mc_t": 0.01,
        # "mc_t": 0.25718313951098054,
        # "mc_t": 0.5,
        "mc_t": 0.9,
        # beginning time, for pathway or for trajectory, exact time = begin_t*tau
        "begin_t": 0.0,
        # end time, for pathway or for trajectory, exact time = end_t*tau
        # here 0.25718313951098054 is actually 0.2 seconds
        # "end_t": 0.01,
        # "end_t": 0.25718313951098054,
        # "end_t": 0.5,
        "end_t": 0.9,
        # "end_t": 1e-6,
        # fix t0 or tf, default t0
        "fixed_t0_or_tf": "t0",
        # species oriented, if true, pick pathways ending with top_n species,
        #  if False, just top n pathway
        "spe_oriented": False,
        # condense species path, no reactions
        "species_path": False,
        # atom followed
        "atom_f": "C",
        # "atom_f": "HA4",
        # "init_s": 60,
        "init_s": 61,
        # "init_s": 62,
        # terminal species for file ./setting.json, either None, or [] or [14, 15]
        "terminal_spe": [],
        # regular expression used to filter pathway when preparing candidate pathways, pandas, str.contains(path_reg)
        # examples are path_reg=None, path_reg='^S62R(736|738)', path_reg='S(25|27)', path_reg='S(39|50)'
        "path_reg": None,
        # "path_reg": 'S(25R|25$|27R|27$|77R|77$)',
        # "path_reg": 'S(39R|39$|50R|50$|76R|76$)',
        # "path_reg": 'S(25R|25$|27R|27$|77R|77$|39R|39$|50R|50$|76R|76$)',
        # another filter for pathway name selction, pathway can not contain this regular expression
        # examples are no_path_reg=None, no_path_reg='S(60R|60$)' or no_path_reg='S(61R|61$)', to exclude primary cycles
        "no_path_reg": None,
        # "no_path_reg": 'R(\d)+S(60R|60$|61R|61$|78R|78$|80R|80$)',
        # initial species index, for species passage time evaluation, either None, or [] or [14, 15]
        "init_s_idx": [],
        # end species index, either None, or [] or [14, 15]
        "end_s_idx": None,
        # "end_s_idx": [25],
        # top n path
        "top_n_p": 100,
        # top n path for gephi to generate coordinates
        "top_n_p_gephi": 500,
        # top n species
        "top_n_s": 5,
        # number of trajectory used to generate pathway list running mc simulation
        "mc_n_traj": 1e8,
        # path integral number of trajectory
        "pi_n_traj": 10000,
        # number of time points when prepare path integral time points
        "pi_n_time": 1,
        # tag, M or fraction
        "tag": "M"
    }
    return setting


def get_chattering_species(atom_followed="C"):
    """
    return chattering species
    the chatteing reaction infomation is just for reference, will not use it
    as long as the paired chattering species is provided, should be fine
    better make them in the same order
    """
    fast_transitions = [
        # {}
        # 1068    549     O2+npropyl=npropyloo
        # reactants       9       O2      60      npropyl products        78      npropyloo
        # 1069    -549    O2+npropyl=npropyloo
        {
            "rxn": [1068, 1069],
            "spe": {
                "H": [60, 78],
                "C": [60, 78],
                "O": [9, 78],
                "HA1": [60, 78],
                "HA2": [60, 78],
                "HA3": [60, 78],
                "HA4": [60, 78],
                "HA5": [60, 78],
                "HA6": [60, 78]
            }
        },


        # 1116    575     O2+QOOH_1=well_1
        # reactants       9       O2      87      QOOH_1  products        90      well_1
        # 1117    -575    O2+QOOH_1=well_1
        {
            "rxn": [1116, 1117],
            "spe": {
                "H": [87, 90],
                "C": [87, 90],
                "O": [9, 90],
                "HA1": [87, 90],
                "HA2": [87, 90],
                "HA3": [87, 90],
                "HA4": [87, 90],
                "HA5": [87, 90],
                "HA6": [87, 90]
            }
        },

        # 1080    556     npropyloo=QOOH_1        557     npropyloo=QOOH_1
        # reactants       78      npropyloo       products        87      QOOH_1
        # 1081    -556    npropyloo=QOOH_1        -557    npropyloo=QOOH_1
        {
            "rxn": [1080, 1081],
            "spe": {
                "H": [78, 87],
                "C": [78, 87],
                "O": [78, 87],
                "HA1": [78, 87],
                "HA2": [78, 87],
                "HA3": [78, 87],
                "HA4": [78, 87],
                "HA5": [78, 87],
                "HA6": [78, 87]
            }
        },

        # 1096    565     O2+ipropyl=ipropyloo
        # reactants       9       O2      61      ipropyl products        80      ipropyloo
        # 1097    -565    O2+ipropyl=ipropyloo
        {
            "rxn": [1096, 1097],
            "spe": {
                "H": [61, 80],
                "C": [61, 80],
                "O": [9, 80],
                "HA1": [61, 80],
                "HA2": [61, 80],
                "HA3": [61, 80],
                "HA4": [61, 80],
                "HA5": [61, 80],
                "HA6": [61, 80]
            }
        },

        # 1124	579	O2 + QOOH_2 = well_2
        # reactants	9	O2	88	QOOH_2	products	91	well_2
        # net_reactants	9	O2	88	QOOH_2	net_products	91	well_2
        {
            "rxn": [1124, 1125],
            "spe": {
                "H": [88, 91],
                "C": [88, 91],
                "O": [9, 91],
                "HA1": [88, 91],
                "HA2": [88, 91],
                "HA3": [88, 91],
                "HA4": [88, 91],
                "HA5": [88, 91],
                "HA6": [88, 91]
            }
        },

        # 1146	590	O2 + QOOH_3 = well_3
        # reactants	9	O2	89	QOOH_3	products	92	well_3
        # net_reactants	9	O2	89	QOOH_3	net_products	92	well_3
        {
            "rxn": [1146, 1147],
            "spe": {
                "H": [89, 92],
                "C": [89, 92],
                "O": [9, 92],
                "HA1": [89, 92],
                "HA2": [89, 92],
                "HA3": [89, 92],
                "HA4": [89, 92],
                "HA5": [89, 92],
                "HA6": [89, 92]
            }
        },

        # # 1214	624	prod_1=frag_1+OH
        # # reactants	94	prod_1	products	10	OH	101	frag_1
        # # net_reactants	94	prod_1	net_products	10	OH	101	frag_1
        # {
        #     "rxn": [1214, 1215],
        #     "spe": {
        #         "H": [94, 101],
        #         "C": [94, 101],
        #         "O": [94, 101],
        #         "HA1": [94, 101],
        #         "HA2": [94, 101],
        #         "HA3": [94, 101],
        #         "HA4": [94, 101],
        #         "HA5": [94, 101],
        #         "HA6": [94, 101]
        #     }
        # },

        # 1042    536     allyloxy=vinoxylmethyl
        # reactants       72      allyloxy        products        108     vinoxylmethyl
        # 1043    -536    allyloxy=vinoxylmethyl
        {
            "rxn": [1042, 1043],
            "spe": {
                "H": [72, 108],
                "C": [72, 108],
                "O": [72, 108],
                "HA1": [72, 108],
                "HA2": [72, 108],
                "HA3": [72, 108],
                "HA4": [72, 108],
                "HA5": [72, 108],
                "HA6": [72, 108]
            }
        },

        # 348     180     C2H5+O2=CH3CH2OO
        # reactants       39      C2H5    9       O2      products        50      CH3CH2OO
        # 349     -180    C2H5+O2=CH3CH2OO
        {
            "rxn": [348, 349],
            "spe": {
                "H": [39, 50],
                "C": [39, 50],
                "O": [9, 50],
                "HA1": [39, 50],
                "HA2": [39, 50],
                "HA3": [39, 50],
                "HA4": [39, 50],
                "HA5": [39, 50],
                "HA6": [39, 50]
            }
        },

        # 132     69      CH3+O2(+M)=CH3OO(+M)
        # reactants       25      CH3     9       O2      products        27      CH3OO
        # 133     -69     CH3+O2(+M)=CH3OO(+M)
        {
            "rxn": [132, 133],
            "spe": {
                "H": [25, 27],
                "C": [25, 27],
                "O": [9, 27],
                "HA1": [25, 27],
                "HA2": [25, 27],
                "HA3": [25, 27],
                "HA4": [25, 27],
                "HA5": [25, 27],
                "HA6": [25, 27]
            }
        },

        # 586     300     O2C2H4OH=CH2CH2OH+O2
        # reactants       85      O2C2H4OH        products        54      CH2CH2OH        9       O2
        # 587     -300    O2C2H4OH=CH2CH2OH+O2
        {
            "rxn": [586, 587],
            "spe": {
                "H": [85, 54],
                "C": [85, 54],
                "O": [85, 9],
                "HA1": [85, 54],
                "HA2": [85, 54],
                "HA3": [85, 54],
                "HA4": [85, 54],
                "HA5": [85, 54],
                "HA6": [85, 54]
            }
        },

        # 434     224     acetyl+O2=acetylperoxy
        # reactants       9       O2      45      acetyl  products        47      acetylperoxy
        # 435     -224    acetyl+O2=acetylperoxy
        {
            "rxn": [434, 435],
            "spe": {
                "H": [45, 47],
                "C": [45, 47],
                "O": [9, 47],
                "HA1": [45, 47],
                "HA2": [45, 47],
                "HA3": [45, 47],
                "HA4": [45, 47],
                "HA5": [45, 47],
                "HA6": [45, 47]
            }
        }

    ]

    trapped_species_list = []
    for _, r_s in enumerate(fast_transitions):
        print(r_s)
        if 'spe' not in r_s:
            continue
        if atom_followed not in r_s['spe']:
            continue
        if len(r_s['spe'][atom_followed]) != 2:
            continue

        trapped_species_list.append(
            [int(r_s['spe'][atom_followed][0]), int(r_s['spe'][atom_followed][1])])
    print(trapped_species_list)

    chattering_species = {}
    for idx, val in enumerate(trapped_species_list):
        print(idx, val)
        chattering_species.update({str(idx + 1): val})

    chattering_species = OrderedDict(chattering_species)
    print(chattering_species)
    return chattering_species


def get_s_a_setting():
    """
    return sensitivity analysis parametes
    """
    setting = {
        # number of runs, number of smaples
        "n_run": 5000,
        # timeout in seconds, if a single mc run longer than this time, terminate it
        "timeout": 300,
        # space dimensionality
        "n_dim": 8,
        # indices that not will not be sampled, either be None, [] or like [0, 2]
        "exclude": [0, 2],
        # parameters used in least square regression
        # number of variables, equals n_dim - len(exclude)
        "N_variable": 8,
        "Nth_order_1st": 2,
        "Nth_order_2nd": 2,

        # parameters used in mc sampling
        "default_uncertainty": 100.0,
        "init_temp": 1000,
        "critical_temp": 1100,
        "end_temp": 1900,
        "target_temp": 1800,

        # species index and concentration, as a nominal initial condition
        "spe_idx_conc": {
            # nominal concentration at time 1.0e-6 seconds
            # "0": 2.25322798606747418e-05,
            # "1": 7.63825332182982599e-15,
            # "2": 4.50645598014366927e-05,
            # "3": 6.55158764564955641e-17,
            # "4": 4.73285585690103025e-15,
            # "5": 9.79463390354316802e-17,
            # "6": 5.45404278306276878e-14,
            # "7": 5.28510891691534245e-16
            # nominal concentration at time 1.0e-5 seconds
            "0": 2.25322792340927307e-05,
            "1": 1.06745743007354256e-13,
            "2": 4.50645594093571151e-05,
            "3": 8.72629092217001897e-15,
            "4": 4.96216242705939368e-15,
            "5": 1.92864677174077298e-16,
            "6": 6.22838831591819596e-13,
            "7": 5.71763673264164999e-16
        }
    }

    return setting


if __name__ == '__main__':
    get_chattering_species("HA2")

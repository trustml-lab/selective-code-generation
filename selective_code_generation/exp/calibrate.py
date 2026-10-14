import math
from .util import clopper_pearson

def calibrate(calibrate_list, epsilon, delta, epsilon_e, add_epsilon_s=False, debug=False):
    U_min = float('inf')

    ds = sorted(calibrate_list, key=lambda d:d['scores'])
    i_under = 1
    i_upper = len(ds)

    log2_Zu = math.ceil(math.log2(len(ds)))
    tau_s_i = None
    
    if debug:
        print('------------start-------------')
        print(f'total len: {len(calibrate_list)}')

    for _ in range(log2_Zu):
        mid = math.ceil((i_under + i_upper ) / 2)
        tau_s_i = ds[mid - 1]['scores']
        Z_u_i = ds[mid - 1:]

        k_i = 0
        for element in Z_u_i:
            if not element['equiv']:
                k_i += 1

        U_i = clopper_pearson(k_i, len(Z_u_i), delta/log2_Zu)
        U_min = min(U_min, U_i)

        if add_epsilon_s:
            upper_bound = U_i + epsilon_e
        else:
            upper_bound = U_i
            
        if upper_bound <= epsilon:
            i_upper = mid
        else:
            i_under = mid

        if debug:
            print('-----------------------------------------------------')
            print(f'k_i: {k_i}, U_min: {U_min}, U_i: {U_i}, mid: {mid}')
            print(f'total: {len(Z_u_i)} non-alpha: {k_i}')
            print('-----------------------------------------------------')

    if debug: 
        print('---------finish---------')
        print(f'tau_s: {tau_s_i}')
    return tau_s_i

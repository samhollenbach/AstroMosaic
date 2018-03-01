import math

def S_N():
    return g * N_netstar / math.sqrt(g * N_netstar + n*g*N_sky + n*sig_read**2)

sig_read = 0

# V FILTER

# V - A
N_netstar = 259584.6
g = 1.0
n = 254.6459
#sig_read = 16.28059
N_sky = 867.4044

print(S_N())

# V - B
N_netstar = 220888.3
g = 1.0
n = 254.5698
#sig_read = 14.10348
N_sky = 862.5959

print(S_N())


# R FILTER

# R - A
N_netstar = 287448
g = 1.0
n = 254.7124
#sig_read = 16.00616
N_sky = 940.9067


print(S_N())

# R - B
N_netstar = 241903.9
g = 1.0
n = 254.7373
#sig_read = 13.97423
N_sky = 942.2166

print(S_N())
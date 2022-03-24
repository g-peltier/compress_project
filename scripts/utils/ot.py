def get_X_Y(df):
    df_num = df.drop(["gez3","teg3"], axis=1)

    Full = df_num.to_numpy(dtype=float)
    mean, std = Full.mean(axis=0), Full.std(axis=0)

    X = (df_num.loc[couple_clean.part1, ].to_numpy(dtype=float) - mean)/std
    Y = (df_num.loc[couple_clean.part2, ].to_numpy(dtype=float) - mean)/std

    return X, Y

def sinkhorn(mu1, mu2, C, epsilon=0.1, max_iters=100):
    """Run Sinnkhorn's algorithm"""
    
    K = np.exp(-C/epsilon)
    
    v = np.ones(b.shape[0])
    err = 1
    for _ in range(max_iters):
        u = a / K.dot(v)
        v = b / K.T.dot(u)
    
    return u, v
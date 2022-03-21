def get_data(pd_df):
    
    inf_cols = [
        "verb_sum",
        "num_sum",
        "spat_sum",
        "mean_max3orig",
        "mean_fluency",
        "TEKintra_mean",
        "TEKinter_mean",
        "SEverb_mean",
        "SEnum_mean",
        "SEspat_mean",
        "SEcrea_mean",
        "SEintra_mean",
        "SEinter_mean",
        "PEverb_mean",
        "PEnum_mean",
        "PEspat_mean",
        "PEcrea_mean",
        "PEintra_mean",
        "PEinter_mean",
        "verb_t_mean",
        "inter_t_mean",
        "verb_t_eff",
        "inter_t_eff",
        "FE_verb_acq_s_1",
        "FE_verb_acq_s_15",
        "SSWK_verbal",
        "SSWK_inter",
        "obs_verb_t_mean",
        "obs_inter_t_mean",
        "obs_verb_t_eff",
        "obs_inter_t_eff"
    ]
    
    return pd_df.set_index("code").loc[:, inf_cols]
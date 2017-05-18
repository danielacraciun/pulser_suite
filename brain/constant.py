hr_ranges = {
    0 : {
        (18, 25): (49, 82),
        (26, 35): (49, 82),
        (36, 45): (50, 83),
        (46, 55): (50, 84),
        (56, 65): (51, 82),
        (65, 200): (50, 80),
    },
    1: {
        (18, 25): (54, 85),
        (26, 35): (54, 83),
        (36, 45): (54, 85),
        (46, 55): (54, 84),
        (56, 65): (54, 84),
        (65, 200): (54, 84),
    }
}

# May be replaced with specific path to train/test ds
train_ds = 'datasets/full_pamap.csv'
test_ds = 'datasets/spare_test.csv'
trained_models_folder = 'trained_models'
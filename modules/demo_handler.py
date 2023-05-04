def calculate_data(input_df):
    # Perform calculations on the input DataFrame
    output_df = input_df.copy()
    output_df['Result'] = output_df['Input'] * 2

    return output_df

import pandas as pd
import plotly.graph_objects as go


# Read json file into df
data = pd.read_json("/Users/anvir9999/Documents/ds3500_23/Artists.json")

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
df


# Extract the birth decade
df['BirthDecade'] = (df['BeginDate'] // 10) * 10

# Drop rows with missing or unknown data (decade is 0)
df = df[(df['BirthDecade'] != 0) & (~df['Nationality'].isna()) & (~df['Gender'].isna())]

# Display the DataFrame
print(df)

# Group by nationality and birth decade, count artists, and reset index
grouped_data = df.groupby(['Nationality', 'BirthDecade']).size().reset_index(name='ArtistCount')
print(grouped_data)

threshold = 20

# Filter rows based on the threshold
filtered_data = grouped_data[grouped_data['ArtistCount'] >= threshold]
print(filtered_data)

# Create a list of unique labels for nodes
labels = pd.concat([filtered_data['Nationality'], filtered_data['BirthDecade']]).unique()


# Create a Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=filtered_data['Nationality'].apply(lambda x: labels.tolist().index(x)),
        target=filtered_data['BirthDecade'].apply(lambda x: labels.tolist().index(x)),
        value=filtered_data['ArtistCount']
    )
))

# Show the Sankey diagram
fig.show()


# Create a DataFrame
df = pd.DataFrame(data)

# Filter rows with missing or unknown data
df = df.dropna(subset=['Nationality', 'Gender'])


grouped_data = df.groupby(['Nationality', 'Gender']).size().reset_index(name='ArtistCount')

# Set the threshold
threshold = 20

# Filter rows based on the threshold
filtered_data = grouped_data[grouped_data['ArtistCount'] >= threshold]

# Create a list of unique labels for nodes
labels = pd.concat([filtered_data['Nationality'], filtered_data['Gender']]).unique()

# Create a Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=filtered_data['Nationality'].apply(lambda x: labels.tolist().index(x)),
        target=filtered_data['Gender'].apply(lambda x: labels.tolist().index(x)),
        value=filtered_data['ArtistCount']
    )
))

# Show the Sankey diagram
fig.show()


# Create a DataFrame
df = pd.DataFrame(data)

# Filter rows with missing or unknown data
df = df.dropna(subset=['Gender', 'BeginDate'])

# Extract the decade of birth
df['BirthDecade'] = (df['BeginDate'] // 10) * 10

# Group by gender and decade of birth, count artists, and reset index
grouped_data = df.groupby(['Gender', 'BirthDecade']).size().reset_index(name='ArtistCount')

# Set the threshold
threshold = 20

# Filter rows based on the threshold
filtered_data = grouped_data[grouped_data['ArtistCount'] >= threshold]

# Create a list of unique labels for nodes
labels = pd.concat([filtered_data['Gender'], filtered_data['BirthDecade']]).unique()

# Create a Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=filtered_data['Gender'].apply(lambda x: labels.tolist().index(x)),
        target=filtered_data['BirthDecade'].apply(lambda x: labels.tolist().index(x)),
        value=filtered_data['ArtistCount']
    )
))

# Show the Sankey diagram
fig.show()


# Define columns
columns = ['Nationality', 'Birth_Decade', 'Gender']

# Create a list of unique labels for nodes
nodes = pd.concat([filtered_data[column] for column in columns]).unique()

# Initialize an empty list to store links
links = []

# Loop through columns to create links
for i in range(len(columns) - 1):
    source_column = columns[i]
    target_column = columns[i + 1]

    for source_value in filtered_data[source_column].unique():
        for target_value in filtered_data[target_column].unique():
            value = len(filtered_data[(filtered_data[source_column] == source_value) & (filtered_data[target_column] == target_value)])

            link = {'source': source_value, 'target': target_value, 'value': value}
            links.append(link)


sankey_trace = go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes
    ),
    link=dict(
        source=[nodes.tolist().index(link['source']) for link in links],
        target=[nodes.tolist().index(link['target']) for link in links],
        value=[link['value'] for link in links],
        color="rgba(0, 128, 128, 0.7)"
    )
)

layout = dict(title="Sankey Diagram")

# Create a Figure
fig = go.Figure(data=[sankey_trace], layout=layout)

# Show the Sankey diagram
fig.show()

if save:
    fig.write_image(save)
else:
    if vals is not None and not vals_empty:
        values = df[vals]
    else:
        values = [10] * len(df)

    num = [1, 2, 1, 5, 12, 4]
    colors = ["lightgreen", "teal", "mediumblue", "mediumslateblue", "violet", "hotpink"]
    colors_list = []

    for i in colors:
        for n in num:
            colors_list.append(i)

    df, labels = _code_mapping(df, src, targ)

    link = {'source': df[src], 'target': df[targ], 'value': values, 'line': {'color': "black", 'width': 1}}

    node_thickness = kwargs.get("node_thickness", 30)

    node = {'label': labels, 'pad': 25, 'thickness': node_thickness, 'line': {'color': "black", 'width': 1}}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    fig.show()

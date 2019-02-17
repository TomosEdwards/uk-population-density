import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# get UK census data into a pandas dataframe from csv downloaded from Census website
df = pd.read_csv('PostcodeDistricts.csv', header=0)

# set a population density variable and covert to persons per km^2 for use later (column name retrieved by df.columns)
pop_density = df['Variable: Density (number of persons per hectare); measures: Value']*0.01

# set shapefile path and create a geopandas dataframe for Postcode District Polygons
sf = r'Distribution/Districts.shp'
gpdf = gpd.read_file(sf)

# Map geopandas dataframe. Initially set to epsg 4632, then transform to epsg 3763 and scale to km^2
gpdf.crs = {'init': 'epsg:4326'}
gpdf.to_crs(epsg=3763, inplace=True)
gpdf.scale(xfact=0.000001, yfact=0.000001, zfact=0.000001)

# Merge the Map and Shapefile data together
data = gpdf.merge(df, left_on='name', right_on='geography code')

# Plot geospatial polygons with the color varying against the log of population density
# Absolute population density didn't give
fig, ax = plt.subplots(1, figsize=(15, 15), constrained_layout=True)
data.plot(column=pop_density.name, cmap= 'coolwarm', linewidth=0.3, ax=ax,
          edgecolor='0.5',
          norm=colors.LogNorm(vmin=pop_density.min(), vmax=pop_density.max())
          )
# Get rid of axes for presentation and add a title
ax.axis('off')
fig.suptitle('Postcode Population Density \n (Person per Hectare)', fontsize=30)

# set scalar-mappable variable for configuring the colour bar scale and generate the colour bar
sm = plt.cm.ScalarMappable(cmap='coolwarm',
                           norm=colors.LogNorm(vmin=pop_density.min(), vmax=pop_density.max())
                           )
sm._A = []
cbar = fig.colorbar(sm)

# Generate chart and save image
fig.show()
fig.savefig('UK Postcode', dpi=300)

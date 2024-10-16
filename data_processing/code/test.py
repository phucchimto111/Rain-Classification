import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Create a plot with Plate Carree projection (for latitude/longitude)
fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': ccrs.PlateCarree()})

# Set the extent (left, right, bottom, top)
ax.set_extent([101.0, 111.0, 17.5, 21.1], crs=ccrs.PlateCarree())

# Draw coastlines for reference
ax.coastlines()

# Plot the rectangle's boundary
ax.plot([101.0, 111.0, 111.0, 101.0, 101.0],  # Longitude points (closing the loop)
        [17.5, 17.5, 21.1, 21.1, 17.5],        # Latitude points
        color='red', linewidth=2, transform=ccrs.PlateCarree())

# Add labels and show the plot
plt.title("Bounding Box: 101.0, 17.5 to 111.0, 21.1")
plt.show()


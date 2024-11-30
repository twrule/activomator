import matplotlib.pyplot as plt
from PIL import Image

class ActivityDrawer:
    def __init__(self):
        black_1 = '#030300'
        black_2 = '#1F1F1E'
        white_1 = '#ECE5D3'

        self.black = black_2
        self.white = white_1
        self.gpx_file = 'activity_drawer/test_file.gpx'
        self.image_path = 'input_image.jpg'
        pass

    def draw_activity(self):
        self._gpx_to_image()
        
        print("Image created successfully")

    def _gpx_to_image(self):
        f = open(self.gpx_file, "r")

        coords = self._get_coords(f)

        self._draw_graph(coords['x'], coords['y'])
        self._add_margins()

    def _get_coords(self, f):
        x_coords = []
        y_coords = []

        for line in f:
            if "<trkpt" in line:
                parts = line.split("\"")
                lon = float(parts[1])
                lat = float(parts[3])
                x_coords.append(lat)
                y_coords.append(lon)
            
        x_coords = list(map(float, x_coords))
        y_coords = list(map(float, y_coords))

        return {"x": self._normalize_coords(x_coords), "y": self._normalize_coords(y_coords)}

    def _normalize_coords(self, coords):
        min_val = min(coords)
        max_val = max(coords)

        norm_coords = [(val - min_val) / (max_val - min_val) for val in coords]

        return norm_coords

    def _draw_graph(self, x_coords, y_coords):
        dpi = 300 

        fig = plt.figure(facecolor=self.white)
        ax = fig.add_subplot(1,1,1)
        ax.scatter(x_coords, y_coords, color=self.black)
        ax.axis('off')
        

        fig.savefig(self.image_path, dpi=dpi, format="jpg", bbox_inches="tight")

    def _add_margins(self):
        original_image = Image.open(self.image_path)
        
        original_width, original_height = original_image.size
        
        top_bottom_margin = (original_height * 2) // 3

        new_height = original_height + 2 * top_bottom_margin
        new_width = original_width  
        
        new_image = Image.new("RGB", (new_width, new_height), color=self.white)
        
        new_image.paste(original_image, (0, top_bottom_margin))
        
        new_image.save(self.image_path)
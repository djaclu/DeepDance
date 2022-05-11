// Ion Class
// An Ion is a type of active cell with extra properties

class Ion {
  PVector position; //XY Coordinates
  PVector velocity;
  PVector acceleration;
  float lifespan;
  int[] rgb;
  boolean active;

  Ion(PVector l, int cell_size) {
    //Vectors between most recent cell and preceding one
    position = l.copy();
    velocity = new PVector(random(-1, 1), random(-2, 0));
    acceleration = new PVector(0, 0.05);
    lifespan = 255.0; //Lag, look at framerate for draw.
    rgb = getColor(l.x/cell_size, l.y/cell_size);
    active = true;
  }

  void run() {
    update();
    display();
  }

  // Method to update position
  void update() {
    velocity.add(acceleration);
    position.add(velocity);
    lifespan -= 1.0;
    rgb = getColor(position.x/cell_size, position.y/cell_size);
  }

  // Method to display
  void display() {
    int[] cell_xy = getCell(position.x, position.y);
    stroke(rgb[0], rgb[1], rgb[2]);
    fill(rgb[0], rgb[1], rgb[2], lifespan);
    square(cell_xy[0], cell_xy[1], cell_size);
  }

  // Method to determine if active
  boolean isActive() {
    if (lifespan > 0.0) {
      active = true;
    } else {
      active = false;
    }
  }
}

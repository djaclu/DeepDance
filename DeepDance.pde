import java.util.*;
import processing.net.*;

//Parameters
int cell_size = 20;
int lag = 300; //in ms
byte delim = (byte)char('}');
int trailing_ions = 3;

//Global Variables
ArrayDeque<int[]> draw_queue = new ArrayDeque<int[]>();
ArrayDeque<int[]> erase_queue = new ArrayDeque<int[]>();
ArrayDeque<Ion[]> ion_queue = new ArrayDeque<Ion[]>();

float h = 1280/cell_size;
float v = 720/cell_size;

float v_gradient = 255/v;
float h_gradient = 255/h;

Server server;

void setup() {
  size(1920, 1080); 
  background(0,0,0);
  
  //Server Setup
  String LocalHost = "127.0.0.1";
  server = new Server(this, 50010, LocalHost);
  
    //Connection Maintenance
  if ((server.active() == true)){
    println("Server Active");
  }
  
  float r = 0;
  float g = 255;
  float b = 255;
  
    for (int i = 0; i<width; i += cell_size){
      b -= h_gradient;
      r = 0;
      g = 255;
      for (int j = 0; j<height; j += cell_size){
        r += v_gradient;
        g -= v_gradient;
        noFill();
        stroke(r, g, b);
        square(i, j, cell_size);
      }
  }
}

void draw() {
  
  //Incoming Data from Beacon Detection
  Client client = server.available();
  
  if (client != null){
    String jsonString = client.readStringUntil(delim);
    JSONObject obj = parseJSONObject(jsonString);
    int x = obj.getInt("x");
    int y = obj.getInt("y");
    get_active_cells(x, y);
  }
  
  get_active_cells(1,1); //ERASE WHEN DONE
  
  //Cell Management
  int dq = draw_queue.size();
  int eq = erase_queue.size();
  int iq = ion_queue.size();
  
  println("dq", dq);
  println("eq", eq);
  
  if (dq > 0){
    //get & draw next cell, add to erase queue
    int[] active_cell = draw_queue.remove();
    noStroke();
    fill(active_cell[2], active_cell[3], active_cell[4]);
    square(active_cell[0], active_cell[1], cell_size);
    erase_queue.addLast(active_cell);
    
    //generate trailing ions
    PVector activeVector = new PVector(active_cell[0], active_cell[1])
    ion = new Ion(activeVector, cell_size)
    
    for (int i = 0; i < trailing_ions; i++){
      ion_queue.addLast(ion);
    }
  }
  
  if (eq > 0){
    //get & erase next cell
    int[] eval_cell = erase_queue.getFirst();
    
    if (millis() - eval_cell[5] > lag){
      int[] unactive_cell = erase_queue.removeFirst();
      fill(0,0,0);
      stroke(unactive_cell[2], unactive_cell[3], unactive_cell[4]);
      square(unactive_cell[0], unactive_cell[1], cell_size);
    }
  }
  
  if(iq > 0){
    //evaluate ion cells
    ion ion_cell = ion_queue.getFirst();
    if ion_cell.isActive(){
      
    }
    
    }
    
}

void get_active_cells(int cursorX, int cursorY) {
  float mouseXcu = mouseX/cell_size; //Cursor X in cell units   //CHANGE WHEN FINISHED
  float mouseYcu = mouseY/cell_size; //Cursor Y in cell units
  
  int cellXcu = Math.round(mouseXcu);
  int cellYcu = Math.round(mouseYcu);
  
  int cellX = cellXcu*cell_size;
  int cellY = cellYcu*cell_size;
  
  int r = 0;
  int g = 255;
  int b = 255;
  
  r += v_gradient * cellYcu;
  g -= v_gradient * cellYcu;
  b -= h_gradient * cellXcu;
  
  int[] active_cell = new int[]{cellX, cellY, r, g, b, millis()};
  
  draw_queue.addLast(active_cell);
}

int[] getCell(int x, int y){
  float Xcu = x/cell_size; //X in cell units
  float Ycu = y/cell_size; //Y in cell units
  
  int cellXcu = Math.round(Xcu);
  int cellYcu = Math.round(Ycu);
  
  int cellX = cellXcu*cell_size;
  int cellY = cellYcu*cell_size;
  
  return new int[] {cellX, cellY};
}

int[] getColor(int cellXcu, int cellYcu){
  int r = 0;
  int g = 255;
  int b = 255;
  
  r += v_gradient * cellYcu;
  g -= v_gradient * cellYcu;
  b -= h_gradient * cellXcu;
  
  return new int[]{r, g, b};
}

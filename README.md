## TrafficSignalControl
Adaptive Traffic Signal Control using YOLO based vehicle detection.<br>
<h5>Introduction:</h5><br>
<p>&nbsp;&nbsp;&nbsp;&nbsp;This system proposes an adaptive traffic control system utilizing the YOLO object detection framework, to provide traffic signal lights at an at-grade four leg intersection with minimum human involvemnet. It uses the YOLOv8 model, trained on our primary dataset, to detect the vehicles on each road at the intersection. This captured information is further passed onto the intersection control algorithm, which then provides the traffic signal.</p>
<h5>Workflow:</h5>



<p>&nbsp;&nbsp;&nbsp;&nbsp;This code uses 4 videos of road to illustrate four camera live camera feed from each road of the intersection. Now from the four roads, it will take a frame from each. Then using the vehicle detection model it will detect and count the number of the vehicles of each road. Now, depending on the number of vehicles , it will provide a dynamic green light time for a road. A road having the green light will be following 3 rules,</p>
<ol>
  <li><strong>Prioritize emergency vehicles:</strong> If there are any emergency vehicles in any of the road , then it will be prioritized to get the green light</li>
  <li><strong>Number of vehicles:</strong> The road with greater number of vehicles will be selected to have green light</li>
  <li><strong>Maintain road cycle:</strong> If a road already happens to have green light once, then it will not have another green light until the other three roads have their green light duration. So, after having a green light, the selection of road is done within the remaining roads</li>
</ol>
Each of the road will follow a formula to calculate the duration of green light,

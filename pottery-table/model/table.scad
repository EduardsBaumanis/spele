// PT-250 / Redakcija B / visas koordinātas cm; 1 vienība = 1 cm.
// Izveidots no source/design.py. Cauruļu stūri un stiprinājumi vienkāršoti.
// Šuves un koka ieliktņu urbumi nav modelēti; rasējumos dotās prasības ir spēkā.
$fn=36;
show_top=true;
show_shelf=true;
show_hardware=true;
exploded=0; // Tikai ilustrācijai; samontētā stāvoklī 0.
top_thickness=5; // Faktiski 4.81..5.15; galda augša paliek Z=78.
shelf_thickness=1.8;
dz=5-top_thickness;
module steel(group) { translate([0,0,dz+(group=="legs"?-exploded*.45:group=="shelf"?-exploded*.7:0)]) color([.73,.12,.08]) children(); }
module washer(x,y,z,od,id,h) {translate([x,y,z]) difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}
module hexnut(x,y,z,af,h,bore) {translate([x,y,z]) difference(){cylinder(d=af/cos(30),h=h,$fn=6);translate([0,0,-.01])cylinder(d=bore,h=h+.02);}}
module bolt(x,y,z,diam,length,af,head) {translate([x,y,z]) {cylinder(d=diam,h=length);translate([0,0,-head])cylinder(d=af/cos(30),h=head,$fn=6);}}
module deck(x,y,z,l,w,t,r) {color([.89,.77,.55]) translate([x,y,z]) linear_extrude(t) hull() for(a=[r,l-r],b=[r,w-r]) translate([a,b]) circle(r=r);}
if(show_top) deck(0,0,78-top_thickness+exploded,250,125,top_thickness,2.5);
if(show_shelf) deck(50,45,23.2+dz-exploded*.7,150,35,shelf_thickness,1);
// T01-1
steel("frame") {
difference(){
translate([18,10,68.8]) cube([214,8,4]);
translate([17.99,10.3,69.1]) cube([214.02,7.4,3.4]);
translate([125,14,68.79]) cylinder(d=0.6,h=0.32);
translate([27,13,68.79]) cylinder(d=3,h=0.32);
translate([223,13,68.79]) cylinder(d=3,h=0.32);
}
}
// T01-2
steel("frame") {
difference(){
translate([18,58.5,68.8]) cube([214,8,4]);
translate([17.99,58.8,69.1]) cube([214.02,7.4,3.4]);
translate([125,62.5,68.79]) cylinder(d=0.6,h=0.32);
}
}
// T01-3
steel("frame") {
difference(){
translate([18,107,68.8]) cube([214,8,4]);
translate([17.99,107.3,69.1]) cube([214.02,7.4,3.4]);
translate([125,111,68.79]) cylinder(d=0.6,h=0.32);
translate([27,112,68.79]) cylinder(d=3,h=0.32);
translate([223,112,68.79]) cylinder(d=3,h=0.32);
}
}
// T02-1
steel("frame") {
difference(){
translate([10,10,68.8]) cube([8,105,4]);
translate([10.3,9.99,69.1]) cube([7.4,105.02,3.4]);
translate([13,13,68.79]) cylinder(d=3,h=0.32);
translate([13,27,68.79]) cylinder(d=3,h=0.32);
translate([13,98,68.79]) cylinder(d=3,h=0.32);
translate([13,112,68.79]) cylinder(d=3,h=0.32);
}
}
// T02-2
steel("frame") {
difference(){
translate([232,10,68.8]) cube([8,105,4]);
translate([232.3,9.99,69.1]) cube([7.4,105.02,3.4]);
translate([237,13,68.79]) cylinder(d=3,h=0.32);
translate([237,27,68.79]) cylinder(d=3,h=0.32);
translate([237,98,68.79]) cylinder(d=3,h=0.32);
translate([237,112,68.79]) cylinder(d=3,h=0.32);
}
}
// T03-1
steel("frame") {
difference(){
translate([62,18,68.8]) cube([6,40.5,4]);
translate([62.3,17.99,69.1]) cube([5.4,40.52,3.4]);
translate([65,38.25,68.79]) cylinder(d=0.6,h=0.32);
}
}
// T03-2
steel("frame") {
difference(){
translate([62,66.5,68.8]) cube([6,40.5,4]);
translate([62.3,66.49,69.1]) cube([5.4,40.52,3.4]);
translate([65,86.75,68.79]) cylinder(d=0.6,h=0.32);
}
}
// T03-3
steel("frame") {
difference(){
translate([182,18,68.8]) cube([6,40.5,4]);
translate([182.3,17.99,69.1]) cube([5.4,40.52,3.4]);
translate([185,38.25,68.79]) cylinder(d=0.6,h=0.32);
}
}
// T03-4
steel("frame") {
difference(){
translate([182,66.5,68.8]) cube([6,40.5,4]);
translate([182.3,66.49,69.1]) cube([5.4,40.52,3.4]);
translate([185,86.75,68.79]) cylinder(d=0.6,h=0.32);
}
}
// P01-F1
steel("frame") {
difference(){
translate([10,10,68]) cube([20,20,0.8]);
translate([13,13,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([13,27,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,13,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,27,67.99]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P01-L1
steel("legs") {
difference(){
translate([10,10,67.2]) cube([20,20,0.8]);
translate([13,13,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([13,27,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,13,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,27,67.19]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// L01-1
steel("legs") {
difference(){
translate([17,17,3.8]) cube([6,6,63.4]);
translate([17.3,17.3,3.79]) cube([5.4,5.4,63.42]);
translate([20,22.69,12.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
translate([20,22.69,25.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
}
}
// P02-1
steel("legs") {
difference(){
translate([17,17,3]) cube([6,6,0.8]);
translate([20,20,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-1-1
steel("legs") {
polyhedron(points=[[23.0, 19.7, 67.2], [29.0, 19.7, 67.2], [23.0, 19.7, 61.2], [23.0, 20.3, 67.2], [29.0, 20.3, 67.2], [23.0, 20.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-1-2
steel("legs") {
polyhedron(points=[[20.3, 23.0, 67.2], [20.3, 29.0, 67.2], [20.3, 23.0, 61.2], [19.7, 23.0, 67.2], [19.7, 29.0, 67.2], [19.7, 23.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-1-3
steel("legs") {
polyhedron(points=[[17.0, 20.3, 67.2], [11.0, 20.3, 67.2], [17.0, 20.3, 61.2], [17.0, 19.7, 67.2], [11.0, 19.7, 67.2], [17.0, 19.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-1-4
steel("legs") {
polyhedron(points=[[19.7, 17.0, 67.2], [19.7, 11.0, 67.2], [19.7, 17.0, 61.2], [20.3, 17.0, 67.2], [20.3, 11.0, 67.2], [20.3, 17.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P03-L1
steel("legs") {
difference(){
translate([17,23,11]) cube([6,0.8,16]);
translate([20,22.99,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([20,22.99,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P03-S1
if(show_shelf) steel("shelf") {
difference(){
translate([17,23.8,11]) cube([6,0.8,16]);
translate([20,23.79,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([20,23.79,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P01-F2
steel("frame") {
difference(){
translate([220,10,68]) cube([20,20,0.8]);
translate([223,13,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([223,27,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,13,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,27,67.99]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P01-L2
steel("legs") {
difference(){
translate([220,10,67.2]) cube([20,20,0.8]);
translate([223,13,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([223,27,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,13,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,27,67.19]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// L01-2
steel("legs") {
difference(){
translate([227,17,3.8]) cube([6,6,63.4]);
translate([227.3,17.3,3.79]) cube([5.4,5.4,63.42]);
translate([230,22.69,12.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
translate([230,22.69,25.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
}
}
// P02-2
steel("legs") {
difference(){
translate([227,17,3]) cube([6,6,0.8]);
translate([230,20,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-2-1
steel("legs") {
polyhedron(points=[[233.0, 19.7, 67.2], [239.0, 19.7, 67.2], [233.0, 19.7, 61.2], [233.0, 20.3, 67.2], [239.0, 20.3, 67.2], [233.0, 20.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-2
steel("legs") {
polyhedron(points=[[230.3, 23.0, 67.2], [230.3, 29.0, 67.2], [230.3, 23.0, 61.2], [229.7, 23.0, 67.2], [229.7, 29.0, 67.2], [229.7, 23.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-3
steel("legs") {
polyhedron(points=[[227.0, 20.3, 67.2], [221.0, 20.3, 67.2], [227.0, 20.3, 61.2], [227.0, 19.7, 67.2], [221.0, 19.7, 67.2], [227.0, 19.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-4
steel("legs") {
polyhedron(points=[[229.7, 17.0, 67.2], [229.7, 11.0, 67.2], [229.7, 17.0, 61.2], [230.3, 17.0, 67.2], [230.3, 11.0, 67.2], [230.3, 17.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P03-L2
steel("legs") {
difference(){
translate([227,23,11]) cube([6,0.8,16]);
translate([230,22.99,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([230,22.99,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P03-S2
if(show_shelf) steel("shelf") {
difference(){
translate([227,23.8,11]) cube([6,0.8,16]);
translate([230,23.79,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([230,23.79,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P01-F3
steel("frame") {
difference(){
translate([10,95,68]) cube([20,20,0.8]);
translate([13,98,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([13,112,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,98,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,112,67.99]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P01-L3
steel("legs") {
difference(){
translate([10,95,67.2]) cube([20,20,0.8]);
translate([13,98,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([13,112,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,98,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([27,112,67.19]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// L01-3
steel("legs") {
difference(){
translate([17,102,3.8]) cube([6,6,63.4]);
translate([17.3,102.3,3.79]) cube([5.4,5.4,63.42]);
translate([20,101.99,12.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
translate([20,101.99,25.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
}
}
// P02-3
steel("legs") {
difference(){
translate([17,102,3]) cube([6,6,0.8]);
translate([20,105,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-3-1
steel("legs") {
polyhedron(points=[[23.0, 104.7, 67.2], [29.0, 104.7, 67.2], [23.0, 104.7, 61.2], [23.0, 105.3, 67.2], [29.0, 105.3, 67.2], [23.0, 105.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-2
steel("legs") {
polyhedron(points=[[20.3, 108.0, 67.2], [20.3, 114.0, 67.2], [20.3, 108.0, 61.2], [19.7, 108.0, 67.2], [19.7, 114.0, 67.2], [19.7, 108.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-3
steel("legs") {
polyhedron(points=[[17.0, 105.3, 67.2], [11.0, 105.3, 67.2], [17.0, 105.3, 61.2], [17.0, 104.7, 67.2], [11.0, 104.7, 67.2], [17.0, 104.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-4
steel("legs") {
polyhedron(points=[[19.7, 102.0, 67.2], [19.7, 96.0, 67.2], [19.7, 102.0, 61.2], [20.3, 102.0, 67.2], [20.3, 96.0, 67.2], [20.3, 102.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P03-L3
steel("legs") {
difference(){
translate([17,101.2,11]) cube([6,0.8,16]);
translate([20,101.19,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([20,101.19,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P03-S3
if(show_shelf) steel("shelf") {
difference(){
translate([17,100.4,11]) cube([6,0.8,16]);
translate([20,100.39,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([20,100.39,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P01-F4
steel("frame") {
difference(){
translate([220,95,68]) cube([20,20,0.8]);
translate([223,98,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([223,112,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,98,67.99]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,112,67.99]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P01-L4
steel("legs") {
difference(){
translate([220,95,67.2]) cube([20,20,0.8]);
translate([223,98,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([223,112,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,98,67.19]) cylinder(d=1.3,h=0.8200000000000001);
translate([237,112,67.19]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// L01-4
steel("legs") {
difference(){
translate([227,102,3.8]) cube([6,6,63.4]);
translate([227.3,102.3,3.79]) cube([5.4,5.4,63.42]);
translate([230,101.99,12.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
translate([230,101.99,25.5]) rotate([-90,0,0]) cylinder(d=3,h=0.32);
}
}
// P02-4
steel("legs") {
difference(){
translate([227,102,3]) cube([6,6,0.8]);
translate([230,105,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-4-1
steel("legs") {
polyhedron(points=[[233.0, 104.7, 67.2], [239.0, 104.7, 67.2], [233.0, 104.7, 61.2], [233.0, 105.3, 67.2], [239.0, 105.3, 67.2], [233.0, 105.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-2
steel("legs") {
polyhedron(points=[[230.3, 108.0, 67.2], [230.3, 114.0, 67.2], [230.3, 108.0, 61.2], [229.7, 108.0, 67.2], [229.7, 114.0, 67.2], [229.7, 108.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-3
steel("legs") {
polyhedron(points=[[227.0, 105.3, 67.2], [221.0, 105.3, 67.2], [227.0, 105.3, 61.2], [227.0, 104.7, 67.2], [221.0, 104.7, 67.2], [227.0, 104.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-4
steel("legs") {
polyhedron(points=[[229.7, 102.0, 67.2], [229.7, 96.0, 67.2], [229.7, 102.0, 61.2], [230.3, 102.0, 67.2], [230.3, 96.0, 67.2], [230.3, 102.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P03-L4
steel("legs") {
difference(){
translate([227,101.2,11]) cube([6,0.8,16]);
translate([230,101.19,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([230,101.19,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// P03-S4
if(show_shelf) steel("shelf") {
difference(){
translate([227,100.4,11]) cube([6,0.8,16]);
translate([230,100.39,12.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
translate([230,100.39,25.5]) rotate([-90,0,0]) cylinder(d=1.3,h=0.8200000000000001);
}
}
// S01-1
if(show_shelf) steel("shelf") {
difference(){
translate([22,45,15]) cube([206,4,8]);
translate([21.99,45.3,15.3]) cube([206.02,3.4,7.4]);
translate([125,47,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S01-2
if(show_shelf) steel("shelf") {
difference(){
translate([22,76,15]) cube([206,4,8]);
translate([21.99,76.3,15.3]) cube([206.02,3.4,7.4]);
translate([125,78,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S02-1
if(show_shelf) steel("shelf") {
difference(){
translate([18,24.6,15]) cube([4,75.8,8]);
translate([18.3,24.59,15.3]) cube([3.4,75.82,7.4]);
translate([20,62.5,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S02-2
if(show_shelf) steel("shelf") {
difference(){
translate([228,24.6,15]) cube([4,75.8,8]);
translate([228.3,24.59,15.3]) cube([3.4,75.82,7.4]);
translate([230,62.5,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-1
if(show_shelf) steel("shelf") {
difference(){
translate([50,49,19]) cube([6,27,4]);
translate([50.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([53,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-2
if(show_shelf) steel("shelf") {
difference(){
translate([68,49,19]) cube([6,27,4]);
translate([68.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([71,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-3
if(show_shelf) steel("shelf") {
difference(){
translate([86,49,19]) cube([6,27,4]);
translate([86.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([89,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-4
if(show_shelf) steel("shelf") {
difference(){
translate([104,49,19]) cube([6,27,4]);
translate([104.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([107,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-5
if(show_shelf) steel("shelf") {
difference(){
translate([122,49,19]) cube([6,27,4]);
translate([122.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([125,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-6
if(show_shelf) steel("shelf") {
difference(){
translate([140,49,19]) cube([6,27,4]);
translate([140.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([143,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-7
if(show_shelf) steel("shelf") {
difference(){
translate([158,49,19]) cube([6,27,4]);
translate([158.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([161,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-8
if(show_shelf) steel("shelf") {
difference(){
translate([176,49,19]) cube([6,27,4]);
translate([176.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([179,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-9
if(show_shelf) steel("shelf") {
difference(){
translate([194,49,19]) cube([6,27,4]);
translate([194.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([197,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// P04-W01-1
steel("frame") {
difference(){
translate([38,18,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([40+dx,20,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-2
steel("frame") {
difference(){
translate([72,18,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([74+dx,20,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-3
steel("frame") {
difference(){
translate([106,18,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([108+dx,20,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-4
steel("frame") {
difference(){
translate([140,18,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([142+dx,20,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-5
steel("frame") {
difference(){
translate([174,18,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([176+dx,20,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-6
steel("frame") {
difference(){
translate([208,18,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([210+dx,20,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-7
steel("frame") {
difference(){
translate([38,103,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([40+dx,105,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-8
steel("frame") {
difference(){
translate([72,103,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([74+dx,105,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-9
steel("frame") {
difference(){
translate([106,103,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([108+dx,105,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-10
steel("frame") {
difference(){
translate([140,103,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([142+dx,105,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-11
steel("frame") {
difference(){
translate([174,103,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([176+dx,105,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W01-12
steel("frame") {
difference(){
translate([208,103,72.4]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([210+dx,105,72.4-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W05-1
if(show_shelf) steel("shelf") {
difference(){
translate([60,49,22.6]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([62+dx,51,22.6-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W05-2
if(show_shelf) steel("shelf") {
difference(){
translate([114,49,22.6]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([116+dx,51,22.6-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W05-3
if(show_shelf) steel("shelf") {
difference(){
translate([186,49,22.6]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([188+dx,51,22.6-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W05-4
if(show_shelf) steel("shelf") {
difference(){
translate([60,72,22.6]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([62+dx,74,22.6-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W05-5
if(show_shelf) steel("shelf") {
difference(){
translate([114,72,22.6]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([116+dx,74,22.6-.01]) cylinder(d=.8,h=.42);
}
}
// P04-W05-6
if(show_shelf) steel("shelf") {
difference(){
translate([186,72,22.6]) cube([4,4,0.4]);
hull() for(dx=[-.4,.4]) translate([188+dx,74,22.6-.01]) cylinder(d=.8,h=.42);
}
}
if(show_hardware) {
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([20,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,20,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(20,20,2.2,2.4,.8,1.6);hexnut(20,20,3.8,2.4,1.3,1.6);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(13,13,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(13,13,66.95,2.4,1.3,.25);bolt(13,13,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(13,27,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(13,27,66.95,2.4,1.3,.25);bolt(13,27,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(27,13,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(27,13,66.95,2.4,1.3,.25);bolt(27,13,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(27,27,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(27,27,66.95,2.4,1.3,.25);bolt(27,27,66.95,1.2,3.5,1.9,.75);}
translate([20,23,12.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,24.85,12.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([20,23,25.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,24.85,25.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([230,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([230,20,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(230,20,2.2,2.4,.8,1.6);hexnut(230,20,3.8,2.4,1.3,1.6);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(223,13,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(223,13,66.95,2.4,1.3,.25);bolt(223,13,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(223,27,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(223,27,66.95,2.4,1.3,.25);bolt(223,27,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(237,13,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(237,13,66.95,2.4,1.3,.25);bolt(237,13,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(237,27,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(237,27,66.95,2.4,1.3,.25);bolt(237,27,66.95,1.2,3.5,1.9,.75);}
translate([230,23,12.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,24.85,12.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([230,23,25.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,24.85,25.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([20,105,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,105,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(20,105,2.2,2.4,.8,1.6);hexnut(20,105,3.8,2.4,1.3,1.6);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(13,98,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(13,98,66.95,2.4,1.3,.25);bolt(13,98,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(13,112,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(13,112,66.95,2.4,1.3,.25);bolt(13,112,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(27,98,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(27,98,66.95,2.4,1.3,.25);bolt(27,98,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(27,112,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(27,112,66.95,2.4,1.3,.25);bolt(27,112,66.95,1.2,3.5,1.9,.75);}
translate([20,102,12.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,100.15,12.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([20,102,25.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,100.15,25.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([230,105,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([230,105,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(230,105,2.2,2.4,.8,1.6);hexnut(230,105,3.8,2.4,1.3,1.6);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(223,98,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(223,98,66.95,2.4,1.3,.25);bolt(223,98,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(223,112,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(223,112,66.95,2.4,1.3,.25);bolt(223,112,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(237,98,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(237,98,66.95,2.4,1.3,.25);bolt(237,98,66.95,1.2,3.5,1.9,.75);}
translate([0,0,dz]) color([.5,.53,.55]) hexnut(237,112,68.8,1.9,1,1.2);
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {washer(237,112,66.95,2.4,1.3,.25);bolt(237,112,66.95,1.2,3.5,1.9,.75);}
translate([230,102,12.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,100.15,12.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([230,102,25.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,100.15,25.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
}

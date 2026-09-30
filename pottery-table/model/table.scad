// PT-250 / Redakcija D / visas koordinātas cm; 1 vienība = 1 cm.
// Izveidots no source/design.py. Cauruļu stūri un stiprinājumi vienkāršoti.
// Šuves nav modelētas; rasējumos dotās prasības ir spēkā. Bez augšējā rāmja.
$fn=36;
show_top=true;
show_shelf=true;
show_hardware=true;
exploded=0; // Tikai ilustrācijai; samontētā stāvoklī 0.
top_thickness=5; // Faktiski 4.81..5.15; galda augša paliek Z=78.
dz=5-top_thickness;
module steel(group) { translate([0,0,(group=="top_hardware"?0:dz)+(group=="legs"?-exploded*.45:group=="shelf"?-exploded*.7:group=="top_hardware"?exploded:0)]) color([.73,.12,.08]) children(); }
module washer(x,y,z,od,id,h) {translate([x,y,z]) difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}
module hexnut(x,y,z,af,h,bore) {translate([x,y,z]) difference(){cylinder(d=af/cos(30),h=h,$fn=6);translate([0,0,-.01])cylinder(d=bore,h=h+.02);}}
module bolt(x,y,z,diam,length,af,head) {translate([x,y,z]) {cylinder(d=diam,h=length);translate([0,0,-head])cylinder(d=af/cos(30),h=head,$fn=6);}}
module deck(x,y,z,l,w,t,r) {color([.89,.77,.55]) translate([x,y,z]) linear_extrude(t) hull() for(a=[r,l-r],b=[r,w-r]) translate([a,b]) circle(r=r);}
if(show_top) difference(){deck(0,0,78-top_thickness+exploded,250,125,top_thickness,2.5);
translate([9,9,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([7,7,77.4+exploded]) cube([4,4,.61]);
translate([9,31,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([7,29,77.4+exploded]) cube([4,4,.61]);
translate([31,9,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([29,7,77.4+exploded]) cube([4,4,.61]);
translate([31,31,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([29,29,77.4+exploded]) cube([4,4,.61]);
translate([219,9,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([217,7,77.4+exploded]) cube([4,4,.61]);
translate([219,31,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([217,29,77.4+exploded]) cube([4,4,.61]);
translate([241,9,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([239,7,77.4+exploded]) cube([4,4,.61]);
translate([241,31,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([239,29,77.4+exploded]) cube([4,4,.61]);
translate([9,94,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([7,92,77.4+exploded]) cube([4,4,.61]);
translate([9,116,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([7,114,77.4+exploded]) cube([4,4,.61]);
translate([31,94,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([29,92,77.4+exploded]) cube([4,4,.61]);
translate([31,116,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([29,114,77.4+exploded]) cube([4,4,.61]);
translate([219,94,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([217,92,77.4+exploded]) cube([4,4,.61]);
translate([219,116,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([217,114,77.4+exploded]) cube([4,4,.61]);
translate([241,94,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([239,92,77.4+exploded]) cube([4,4,.61]);
translate([241,116,78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);
translate([239,114,77.4+exploded]) cube([4,4,.61]);
}
// P01-1
steel("legs") {
difference(){
translate([5,5,72.2]) cube([30,30,0.8]);
translate([9,9,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([9,31,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([31,9,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([31,31,72.19]) cylinder(d=1.05,h=0.8200000000000001);
}
}
// P06-1-1
if(show_top) steel("top_hardware") {
difference(){
translate([7,7,77.4]) cube([4,4,0.6]);
translate([9,9,77.39]) cylinder(d=1.05,h=0.62);
translate([9,9,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-1-2
if(show_top) steel("top_hardware") {
difference(){
translate([7,29,77.4]) cube([4,4,0.6]);
translate([9,31,77.39]) cylinder(d=1.05,h=0.62);
translate([9,31,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-1-3
if(show_top) steel("top_hardware") {
difference(){
translate([29,7,77.4]) cube([4,4,0.6]);
translate([31,9,77.39]) cylinder(d=1.05,h=0.62);
translate([31,9,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-1-4
if(show_top) steel("top_hardware") {
difference(){
translate([29,29,77.4]) cube([4,4,0.6]);
translate([31,31,77.39]) cylinder(d=1.05,h=0.62);
translate([31,31,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// L01-1
steel("legs") {
difference(){
translate([17,17,3.8]) cube([6,6,68.4]);
translate([17.3,17.3,3.79]) cube([5.4,5.4,68.42]);
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
polyhedron(points=[[23.0, 19.7, 72.2], [34.0, 19.7, 72.2], [23.0, 19.7, 61.2], [23.0, 20.3, 72.2], [34.0, 20.3, 72.2], [23.0, 20.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-1-2
steel("legs") {
polyhedron(points=[[20.3, 23.0, 72.2], [20.3, 34.0, 72.2], [20.3, 23.0, 61.2], [19.7, 23.0, 72.2], [19.7, 34.0, 72.2], [19.7, 23.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-1-3
steel("legs") {
polyhedron(points=[[17.0, 20.3, 72.2], [6.0, 20.3, 72.2], [17.0, 20.3, 61.2], [17.0, 19.7, 72.2], [6.0, 19.7, 72.2], [17.0, 19.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-1-4
steel("legs") {
polyhedron(points=[[19.7, 17.0, 72.2], [19.699999999999996, 6.0, 72.2], [19.7, 17.0, 61.2], [20.3, 17.0, 72.2], [20.299999999999997, 6.0, 72.2], [20.3, 17.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
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
// P01-2
steel("legs") {
difference(){
translate([215,5,72.2]) cube([30,30,0.8]);
translate([219,9,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([219,31,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([241,9,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([241,31,72.19]) cylinder(d=1.05,h=0.8200000000000001);
}
}
// P06-2-1
if(show_top) steel("top_hardware") {
difference(){
translate([217,7,77.4]) cube([4,4,0.6]);
translate([219,9,77.39]) cylinder(d=1.05,h=0.62);
translate([219,9,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-2-2
if(show_top) steel("top_hardware") {
difference(){
translate([217,29,77.4]) cube([4,4,0.6]);
translate([219,31,77.39]) cylinder(d=1.05,h=0.62);
translate([219,31,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-2-3
if(show_top) steel("top_hardware") {
difference(){
translate([239,7,77.4]) cube([4,4,0.6]);
translate([241,9,77.39]) cylinder(d=1.05,h=0.62);
translate([241,9,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-2-4
if(show_top) steel("top_hardware") {
difference(){
translate([239,29,77.4]) cube([4,4,0.6]);
translate([241,31,77.39]) cylinder(d=1.05,h=0.62);
translate([241,31,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// L01-2
steel("legs") {
difference(){
translate([227,17,3.8]) cube([6,6,68.4]);
translate([227.3,17.3,3.79]) cube([5.4,5.4,68.42]);
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
polyhedron(points=[[233.0, 19.7, 72.2], [244.0, 19.7, 72.2], [233.0, 19.7, 61.2], [233.0, 20.3, 72.2], [244.0, 20.3, 72.2], [233.0, 20.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-2
steel("legs") {
polyhedron(points=[[230.3, 23.0, 72.2], [230.3, 34.0, 72.2], [230.3, 23.0, 61.2], [229.7, 23.0, 72.2], [229.7, 34.0, 72.2], [229.7, 23.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-3
steel("legs") {
polyhedron(points=[[227.0, 20.3, 72.2], [216.0, 20.3, 72.2], [227.0, 20.3, 61.2], [227.0, 19.7, 72.2], [216.0, 19.7, 72.2], [227.0, 19.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-4
steel("legs") {
polyhedron(points=[[229.7, 17.0, 72.2], [229.7, 6.0, 72.2], [229.7, 17.0, 61.2], [230.3, 17.0, 72.2], [230.3, 6.0, 72.2], [230.3, 17.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
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
// P01-3
steel("legs") {
difference(){
translate([5,90,72.2]) cube([30,30,0.8]);
translate([9,94,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([9,116,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([31,94,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([31,116,72.19]) cylinder(d=1.05,h=0.8200000000000001);
}
}
// P06-3-1
if(show_top) steel("top_hardware") {
difference(){
translate([7,92,77.4]) cube([4,4,0.6]);
translate([9,94,77.39]) cylinder(d=1.05,h=0.62);
translate([9,94,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-3-2
if(show_top) steel("top_hardware") {
difference(){
translate([7,114,77.4]) cube([4,4,0.6]);
translate([9,116,77.39]) cylinder(d=1.05,h=0.62);
translate([9,116,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-3-3
if(show_top) steel("top_hardware") {
difference(){
translate([29,92,77.4]) cube([4,4,0.6]);
translate([31,94,77.39]) cylinder(d=1.05,h=0.62);
translate([31,94,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-3-4
if(show_top) steel("top_hardware") {
difference(){
translate([29,114,77.4]) cube([4,4,0.6]);
translate([31,116,77.39]) cylinder(d=1.05,h=0.62);
translate([31,116,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// L01-3
steel("legs") {
difference(){
translate([17,102,3.8]) cube([6,6,68.4]);
translate([17.3,102.3,3.79]) cube([5.4,5.4,68.42]);
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
polyhedron(points=[[23.0, 104.7, 72.2], [34.0, 104.7, 72.2], [23.0, 104.7, 61.2], [23.0, 105.3, 72.2], [34.0, 105.3, 72.2], [23.0, 105.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-2
steel("legs") {
polyhedron(points=[[20.3, 108.0, 72.2], [20.3, 119.0, 72.2], [20.3, 108.0, 61.2], [19.7, 108.0, 72.2], [19.7, 119.0, 72.2], [19.7, 108.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-3
steel("legs") {
polyhedron(points=[[17.0, 105.3, 72.2], [6.0, 105.3, 72.2], [17.0, 105.3, 61.2], [17.0, 104.7, 72.2], [6.0, 104.7, 72.2], [17.0, 104.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-4
steel("legs") {
polyhedron(points=[[19.7, 102.0, 72.2], [19.699999999999996, 91.0, 72.2], [19.7, 102.0, 61.2], [20.3, 102.0, 72.2], [20.299999999999997, 91.0, 72.2], [20.3, 102.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
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
// P01-4
steel("legs") {
difference(){
translate([215,90,72.2]) cube([30,30,0.8]);
translate([219,94,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([219,116,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([241,94,72.19]) cylinder(d=1.05,h=0.8200000000000001);
translate([241,116,72.19]) cylinder(d=1.05,h=0.8200000000000001);
}
}
// P06-4-1
if(show_top) steel("top_hardware") {
difference(){
translate([217,92,77.4]) cube([4,4,0.6]);
translate([219,94,77.39]) cylinder(d=1.05,h=0.62);
translate([219,94,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-4-2
if(show_top) steel("top_hardware") {
difference(){
translate([217,114,77.4]) cube([4,4,0.6]);
translate([219,116,77.39]) cylinder(d=1.05,h=0.62);
translate([219,116,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-4-3
if(show_top) steel("top_hardware") {
difference(){
translate([239,92,77.4]) cube([4,4,0.6]);
translate([241,94,77.39]) cylinder(d=1.05,h=0.62);
translate([241,94,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// P06-4-4
if(show_top) steel("top_hardware") {
difference(){
translate([239,114,77.4]) cube([4,4,0.6]);
translate([241,116,77.39]) cylinder(d=1.05,h=0.62);
translate([241,116,77.5]) cylinder(d1=1,d2=2,h=.5);
}
}
// L01-4
steel("legs") {
difference(){
translate([227,102,3.8]) cube([6,6,68.4]);
translate([227.3,102.3,3.79]) cube([5.4,5.4,68.42]);
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
polyhedron(points=[[233.0, 104.7, 72.2], [244.0, 104.7, 72.2], [233.0, 104.7, 61.2], [233.0, 105.3, 72.2], [244.0, 105.3, 72.2], [233.0, 105.3, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-2
steel("legs") {
polyhedron(points=[[230.3, 108.0, 72.2], [230.3, 119.0, 72.2], [230.3, 108.0, 61.2], [229.7, 108.0, 72.2], [229.7, 119.0, 72.2], [229.7, 108.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-3
steel("legs") {
polyhedron(points=[[227.0, 105.3, 72.2], [216.0, 105.3, 72.2], [227.0, 105.3, 61.2], [227.0, 104.7, 72.2], [216.0, 104.7, 72.2], [227.0, 104.7, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-4
steel("legs") {
polyhedron(points=[[229.7, 102.0, 72.2], [229.7, 91.0, 72.2], [229.7, 102.0, 61.2], [230.3, 102.0, 72.2], [230.3, 91.0, 72.2], [230.3, 102.0, 61.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
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
translate([62,49,19]) cube([6,27,4]);
translate([62.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([65,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-3
if(show_shelf) steel("shelf") {
difference(){
translate([74,49,19]) cube([6,27,4]);
translate([74.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([77,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-4
if(show_shelf) steel("shelf") {
difference(){
translate([86,49,19]) cube([6,27,4]);
translate([86.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([89,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-5
if(show_shelf) steel("shelf") {
difference(){
translate([98,49,19]) cube([6,27,4]);
translate([98.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([101,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-6
if(show_shelf) steel("shelf") {
difference(){
translate([110,49,19]) cube([6,27,4]);
translate([110.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([113,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-7
if(show_shelf) steel("shelf") {
difference(){
translate([122,49,19]) cube([6,27,4]);
translate([122.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([125,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-8
if(show_shelf) steel("shelf") {
difference(){
translate([134,49,19]) cube([6,27,4]);
translate([134.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([137,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-9
if(show_shelf) steel("shelf") {
difference(){
translate([146,49,19]) cube([6,27,4]);
translate([146.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([149,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-10
if(show_shelf) steel("shelf") {
difference(){
translate([158,49,19]) cube([6,27,4]);
translate([158.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([161,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-11
if(show_shelf) steel("shelf") {
difference(){
translate([170,49,19]) cube([6,27,4]);
translate([170.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([173,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-12
if(show_shelf) steel("shelf") {
difference(){
translate([182,49,19]) cube([6,27,4]);
translate([182.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([185,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-13
if(show_shelf) steel("shelf") {
difference(){
translate([194,49,19]) cube([6,27,4]);
translate([194.3,48.99,19.3]) cube([5.4,27.02,3.4]);
translate([197,62.5,18.99]) cylinder(d=0.6,h=0.32);
}
}
if(show_hardware) {
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([20,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,20,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(20,20,2.2,2.4,.8,1.6);hexnut(20,20,3.8,2.4,1.3,1.6);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(9,9,72,2,1.05,.2);hexnut(9,9,71,1.7,1,1);}
if(show_top) translate([9,9,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(9,31,72,2,1.05,.2);hexnut(9,31,71,1.7,1,1);}
if(show_top) translate([9,31,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(31,9,72,2,1.05,.2);hexnut(31,9,71,1.7,1,1);}
if(show_top) translate([31,9,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(31,31,72,2,1.05,.2);hexnut(31,31,71,1.7,1,1);}
if(show_top) translate([31,31,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([20,23,12.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,24.85,12.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([20,23,25.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,24.85,25.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([230,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([230,20,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(230,20,2.2,2.4,.8,1.6);hexnut(230,20,3.8,2.4,1.3,1.6);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(219,9,72,2,1.05,.2);hexnut(219,9,71,1.7,1,1);}
if(show_top) translate([219,9,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(219,31,72,2,1.05,.2);hexnut(219,31,71,1.7,1,1);}
if(show_top) translate([219,31,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(241,9,72,2,1.05,.2);hexnut(241,9,71,1.7,1,1);}
if(show_top) translate([241,9,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(241,31,72,2,1.05,.2);hexnut(241,31,71,1.7,1,1);}
if(show_top) translate([241,31,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([230,23,12.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,24.85,12.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([230,23,25.5+dz-exploded*.45]) rotate([90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,24.85,25.5+dz-exploded*.7]) rotate([90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([20,105,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,105,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(20,105,2.2,2.4,.8,1.6);hexnut(20,105,3.8,2.4,1.3,1.6);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(9,94,72,2,1.05,.2);hexnut(9,94,71,1.7,1,1);}
if(show_top) translate([9,94,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(9,116,72,2,1.05,.2);hexnut(9,116,71,1.7,1,1);}
if(show_top) translate([9,116,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(31,94,72,2,1.05,.2);hexnut(31,94,71,1.7,1,1);}
if(show_top) translate([31,94,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(31,116,72,2,1.05,.2);hexnut(31,116,71,1.7,1,1);}
if(show_top) translate([31,116,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([20,102,12.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,100.15,12.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([20,102,25.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([20,100.15,25.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([0,0,-exploded*.45]) { color([.2,.23,.24]) translate([230,105,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([230,105,2]) cylinder(d=1.6,h=6); }
translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {hexnut(230,105,2.2,2.4,.8,1.6);hexnut(230,105,3.8,2.4,1.3,1.6);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(219,94,72,2,1.05,.2);hexnut(219,94,71,1.7,1,1);}
if(show_top) translate([219,94,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(219,116,72,2,1.05,.2);hexnut(219,116,71,1.7,1,1);}
if(show_top) translate([219,116,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(241,94,72,2,1.05,.2);hexnut(241,94,71,1.7,1,1);}
if(show_top) translate([241,94,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {washer(241,116,72,2,1.05,.2);hexnut(241,116,71,1.7,1,1);}
if(show_top) translate([241,116,exploded]) color([.6,.62,.63]) {translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}
translate([230,102,12.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,100.15,12.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
translate([230,102,25.5+dz-exploded*.45]) rotate([-90,0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);
if(show_shelf) translate([230,100.15,25.5+dz-exploded*.7]) rotate([-90,0,0]) color([.6,.62,.63]) {washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}
}

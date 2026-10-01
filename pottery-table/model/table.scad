// PT-200 / Redakcija F / visas koordinātas cm; 1 vienība = 1 cm.
// Izveidots no source/design.py. Cauruļu stūri un stiprinājumi vienkāršoti.
// Šuves nav modelētas; rasējumos dotās prasības ir spēkā. Bez augšējā rāmja.
$fn=36;
show_top=true;
show_shelf=true;
show_hardware=true;
exploded=0; // Tikai ilustrācijai; samontētā stāvoklī 0.
top_thickness=5; // Faktiski 4.81..5.15; galda augša paliek Z=78.
dz=5-top_thickness;
module steel(group) { translate([0,0,dz]) color([.73,.12,.08]) children(); }
module washer(x,y,z,od,id,h) {translate([x,y,z]) difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}
module hexnut(x,y,z,af,h,bore) {translate([x,y,z]) difference(){cylinder(d=af/cos(30),h=h,$fn=6);translate([0,0,-.01])cylinder(d=bore,h=h+.02);}}
module bolt(x,y,z,diam,length,af,head) {translate([x,y,z]) {cylinder(d=diam,h=length);translate([0,0,-head])cylinder(d=af/cos(30),h=head,$fn=6);}}
module deck(x,y,z,l,w,t,r) {color([.89,.77,.55]) translate([x,y,z]) linear_extrude(t) hull() for(a=[r,l-r],b=[r,w-r]) translate([a,b]) circle(r=r);}
pilot_diameter=.5; // Ilustratīvi; priekšurbuma Ø pēc kokskrūves ražotāja.
if(show_top) difference(){deck(0,0,78-top_thickness+exploded,200,100,top_thickness,2.5);
translate([13,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([13,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([173,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([173,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([187,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([187,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([13,73,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([13,87,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,73,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,87,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([173,73,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([173,87,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([187,73,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([187,87,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
}
// P01-1
steel("legs") {
difference(){
translate([10,10,72.2]) cube([20,20,0.8]);
translate([13,13,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([13,27,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([27,13,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([27,27,72.19]) cylinder(d=0.9,h=0.8200000000000001);
}
}
// L01-1
steel("legs") {
difference(){
translate([17,17,3.8]) cube([6,6,68.4]);
translate([17.3,17.3,3.79]) cube([5.4,5.4,68.42]);
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
polyhedron(points=[[23.0, 19.7, 72.2], [29.0, 19.7, 72.2], [23.0, 19.7, 66.2], [23.0, 20.3, 72.2], [29.0, 20.3, 72.2], [23.0, 20.3, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-1-2
steel("legs") {
polyhedron(points=[[20.3, 23.0, 72.2], [20.3, 29.0, 72.2], [20.3, 23.0, 66.2], [19.7, 23.0, 72.2], [19.7, 29.0, 72.2], [19.7, 23.0, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P01-2
steel("legs") {
difference(){
translate([170,10,72.2]) cube([20,20,0.8]);
translate([173,13,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([173,27,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([187,13,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([187,27,72.19]) cylinder(d=0.9,h=0.8200000000000001);
}
}
// L01-2
steel("legs") {
difference(){
translate([177,17,3.8]) cube([6,6,68.4]);
translate([177.3,17.3,3.79]) cube([5.4,5.4,68.42]);
}
}
// P02-2
steel("legs") {
difference(){
translate([177,17,3]) cube([6,6,0.8]);
translate([180,20,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-2-3
steel("legs") {
polyhedron(points=[[177.0, 20.3, 72.2], [171.0, 20.3, 72.2], [177.0, 20.3, 66.2], [177.0, 19.7, 72.2], [171.0, 19.7, 72.2], [177.0, 19.7, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-2
steel("legs") {
polyhedron(points=[[180.3, 23.0, 72.2], [180.3, 29.0, 72.2], [180.3, 23.0, 66.2], [179.7, 23.0, 72.2], [179.7, 29.0, 72.2], [179.7, 23.0, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P01-3
steel("legs") {
difference(){
translate([10,70,72.2]) cube([20,20,0.8]);
translate([13,73,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([13,87,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([27,73,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([27,87,72.19]) cylinder(d=0.9,h=0.8200000000000001);
}
}
// L01-3
steel("legs") {
difference(){
translate([17,77,3.8]) cube([6,6,68.4]);
translate([17.3,77.3,3.79]) cube([5.4,5.4,68.42]);
}
}
// P02-3
steel("legs") {
difference(){
translate([17,77,3]) cube([6,6,0.8]);
translate([20,80,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-3-1
steel("legs") {
polyhedron(points=[[23.0, 79.7, 72.2], [29.0, 79.7, 72.2], [23.0, 79.7, 66.2], [23.0, 80.3, 72.2], [29.0, 80.3, 72.2], [23.0, 80.3, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-4
steel("legs") {
polyhedron(points=[[19.7, 77.0, 72.2], [19.7, 71.0, 72.2], [19.7, 77.0, 66.2], [20.3, 77.0, 72.2], [20.3, 71.0, 72.2], [20.3, 77.0, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P01-4
steel("legs") {
difference(){
translate([170,70,72.2]) cube([20,20,0.8]);
translate([173,73,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([173,87,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([187,73,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([187,87,72.19]) cylinder(d=0.9,h=0.8200000000000001);
}
}
// L01-4
steel("legs") {
difference(){
translate([177,77,3.8]) cube([6,6,68.4]);
translate([177.3,77.3,3.79]) cube([5.4,5.4,68.42]);
}
}
// P02-4
steel("legs") {
difference(){
translate([177,77,3]) cube([6,6,0.8]);
translate([180,80,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-4-3
steel("legs") {
polyhedron(points=[[177.0, 80.3, 72.2], [171.0, 80.3, 72.2], [177.0, 80.3, 66.2], [177.0, 79.7, 72.2], [171.0, 79.7, 72.2], [177.0, 79.7, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-4
steel("legs") {
polyhedron(points=[[179.7, 77.0, 72.2], [179.7, 71.0, 72.2], [179.7, 77.0, 66.2], [180.3, 77.0, 72.2], [180.3, 71.0, 72.2], [180.3, 77.0, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// S01-1
if(show_shelf) steel("shelf") {
difference(){
translate([22,32.5,15]) cube([156,4,8]);
translate([21.99,32.8,15.3]) cube([156.02,3.4,7.4]);
translate([100,34.5,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S01-2
if(show_shelf) steel("shelf") {
difference(){
translate([22,63.5,15]) cube([156,4,8]);
translate([21.99,63.8,15.3]) cube([156.02,3.4,7.4]);
translate([100,65.5,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S02-1
if(show_shelf) steel("shelf") {
difference(){
translate([18,23,15]) cube([4,54,8]);
translate([18.3,22.99,15.3]) cube([3.4,54.02,7.4]);
translate([20,50,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S02-2
if(show_shelf) steel("shelf") {
difference(){
translate([178,23,15]) cube([4,54,8]);
translate([178.3,22.99,15.3]) cube([3.4,54.02,7.4]);
translate([180,50,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-1
if(show_shelf) steel("shelf") {
difference(){
translate([25,36.5,19]) cube([6,27,4]);
translate([25.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([28,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-2
if(show_shelf) steel("shelf") {
difference(){
translate([37,36.5,19]) cube([6,27,4]);
translate([37.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([40,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-3
if(show_shelf) steel("shelf") {
difference(){
translate([49,36.5,19]) cube([6,27,4]);
translate([49.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([52,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-4
if(show_shelf) steel("shelf") {
difference(){
translate([61,36.5,19]) cube([6,27,4]);
translate([61.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([64,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-5
if(show_shelf) steel("shelf") {
difference(){
translate([73,36.5,19]) cube([6,27,4]);
translate([73.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([76,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-6
if(show_shelf) steel("shelf") {
difference(){
translate([85,36.5,19]) cube([6,27,4]);
translate([85.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([88,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-7
if(show_shelf) steel("shelf") {
difference(){
translate([97,36.5,19]) cube([6,27,4]);
translate([97.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([100,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-8
if(show_shelf) steel("shelf") {
difference(){
translate([109,36.5,19]) cube([6,27,4]);
translate([109.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([112,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-9
if(show_shelf) steel("shelf") {
difference(){
translate([121,36.5,19]) cube([6,27,4]);
translate([121.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([124,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-10
if(show_shelf) steel("shelf") {
difference(){
translate([133,36.5,19]) cube([6,27,4]);
translate([133.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([136,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-11
if(show_shelf) steel("shelf") {
difference(){
translate([145,36.5,19]) cube([6,27,4]);
translate([145.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([148,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-12
if(show_shelf) steel("shelf") {
difference(){
translate([157,36.5,19]) cube([6,27,4]);
translate([157.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([160,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
// S03-13
if(show_shelf) steel("shelf") {
difference(){
translate([169,36.5,19]) cube([6,27,4]);
translate([169.3,36.49,19.3]) cube([5.4,27.02,3.4]);
translate([172,50,18.99]) cylinder(d=0.6,h=0.32);
}
}
if(show_hardware) {
color([.2,.23,.24]) translate([20,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,20,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(20,20,2.2,2.4,.8,1.6);hexnut(20,20,3.8,2.4,1.3,1.6);}
color([.2,.23,.24]) translate([180,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([180,20,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(180,20,2.2,2.4,.8,1.6);hexnut(180,20,3.8,2.4,1.3,1.6);}
color([.2,.23,.24]) translate([20,80,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,80,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(20,80,2.2,2.4,.8,1.6);hexnut(20,80,3.8,2.4,1.3,1.6);}
color([.2,.23,.24]) translate([180,80,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([180,80,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(180,80,2.2,2.4,.8,1.6);hexnut(180,80,3.8,2.4,1.3,1.6);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,13,72,2,.9,.2);bolt(13,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,27,72,2,.9,.2);bolt(13,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,13,72,2,.9,.2);bolt(27,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,27,72,2,.9,.2);bolt(27,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(173,13,72,2,.9,.2);bolt(173,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(173,27,72,2,.9,.2);bolt(173,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(187,13,72,2,.9,.2);bolt(187,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(187,27,72,2,.9,.2);bolt(187,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,73,72,2,.9,.2);bolt(13,73,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,87,72,2,.9,.2);bolt(13,87,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,73,72,2,.9,.2);bolt(27,73,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,87,72,2,.9,.2);bolt(27,87,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(173,73,72,2,.9,.2);bolt(173,73,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(173,87,72,2,.9,.2);bolt(173,87,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(187,73,72,2,.9,.2);bolt(187,73,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(187,87,72,2,.9,.2);bolt(187,87,72,.8,4,1.3,.55);}
}

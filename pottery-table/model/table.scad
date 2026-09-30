// PT-250 / Redakcija E / visas koordinātas cm; 1 vienība = 1 cm.
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
if(show_top) difference(){deck(0,0,78-top_thickness+exploded,250,125,top_thickness,2.5);
translate([13,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([13,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([223,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([223,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([237,13,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([237,27,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([13,98,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([13,112,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,98,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([27,112,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([223,98,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([223,112,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([237,98,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
translate([237,112,78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);
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
translate([220,10,72.2]) cube([20,20,0.8]);
translate([223,13,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([223,27,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([237,13,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([237,27,72.19]) cylinder(d=0.9,h=0.8200000000000001);
}
}
// L01-2
steel("legs") {
difference(){
translate([227,17,3.8]) cube([6,6,68.4]);
translate([227.3,17.3,3.79]) cube([5.4,5.4,68.42]);
}
}
// P02-2
steel("legs") {
difference(){
translate([227,17,3]) cube([6,6,0.8]);
translate([230,20,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-2-3
steel("legs") {
polyhedron(points=[[227.0, 20.3, 72.2], [221.0, 20.3, 72.2], [227.0, 20.3, 66.2], [227.0, 19.7, 72.2], [221.0, 19.7, 72.2], [227.0, 19.7, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-2-2
steel("legs") {
polyhedron(points=[[230.3, 23.0, 72.2], [230.3, 29.0, 72.2], [230.3, 23.0, 66.2], [229.7, 23.0, 72.2], [229.7, 29.0, 72.2], [229.7, 23.0, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P01-3
steel("legs") {
difference(){
translate([10,95,72.2]) cube([20,20,0.8]);
translate([13,98,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([13,112,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([27,98,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([27,112,72.19]) cylinder(d=0.9,h=0.8200000000000001);
}
}
// L01-3
steel("legs") {
difference(){
translate([17,102,3.8]) cube([6,6,68.4]);
translate([17.3,102.3,3.79]) cube([5.4,5.4,68.42]);
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
polyhedron(points=[[23.0, 104.7, 72.2], [29.0, 104.7, 72.2], [23.0, 104.7, 66.2], [23.0, 105.3, 72.2], [29.0, 105.3, 72.2], [23.0, 105.3, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-3-4
steel("legs") {
polyhedron(points=[[19.7, 102.0, 72.2], [19.7, 96.0, 72.2], [19.7, 102.0, 66.2], [20.3, 102.0, 72.2], [20.3, 96.0, 72.2], [20.3, 102.0, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P01-4
steel("legs") {
difference(){
translate([220,95,72.2]) cube([20,20,0.8]);
translate([223,98,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([223,112,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([237,98,72.19]) cylinder(d=0.9,h=0.8200000000000001);
translate([237,112,72.19]) cylinder(d=0.9,h=0.8200000000000001);
}
}
// L01-4
steel("legs") {
difference(){
translate([227,102,3.8]) cube([6,6,68.4]);
translate([227.3,102.3,3.79]) cube([5.4,5.4,68.42]);
}
}
// P02-4
steel("legs") {
difference(){
translate([227,102,3]) cube([6,6,0.8]);
translate([230,105,2.99]) cylinder(d=1.8,h=0.8200000000000001);
}
}
// P05-4-3
steel("legs") {
polyhedron(points=[[227.0, 105.3, 72.2], [221.0, 105.3, 72.2], [227.0, 105.3, 66.2], [227.0, 104.7, 72.2], [221.0, 104.7, 72.2], [227.0, 104.7, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
}
// P05-4-4
steel("legs") {
polyhedron(points=[[229.7, 102.0, 72.2], [229.7, 96.0, 72.2], [229.7, 102.0, 66.2], [230.3, 102.0, 72.2], [230.3, 96.0, 72.2], [230.3, 102.0, 66.2]],faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);
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
translate([18,23,15]) cube([4,79,8]);
translate([18.3,22.99,15.3]) cube([3.4,79.02,7.4]);
translate([20,62.5,14.99]) cylinder(d=0.6,h=0.32);
}
}
// S02-2
if(show_shelf) steel("shelf") {
difference(){
translate([228,23,15]) cube([4,79,8]);
translate([228.3,22.99,15.3]) cube([3.4,79.02,7.4]);
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
color([.2,.23,.24]) translate([20,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,20,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(20,20,2.2,2.4,.8,1.6);hexnut(20,20,3.8,2.4,1.3,1.6);}
color([.2,.23,.24]) translate([230,20,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([230,20,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(230,20,2.2,2.4,.8,1.6);hexnut(230,20,3.8,2.4,1.3,1.6);}
color([.2,.23,.24]) translate([20,105,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([20,105,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(20,105,2.2,2.4,.8,1.6);hexnut(20,105,3.8,2.4,1.3,1.6);}
color([.2,.23,.24]) translate([230,105,0]) cylinder(d=8,h=2);
color([.6,.62,.63]) translate([230,105,2]) cylinder(d=1.6,h=6);
translate([0,0,dz]) color([.6,.62,.63]) {hexnut(230,105,2.2,2.4,.8,1.6);hexnut(230,105,3.8,2.4,1.3,1.6);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,13,72,2,.9,.2);bolt(13,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,27,72,2,.9,.2);bolt(13,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,13,72,2,.9,.2);bolt(27,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,27,72,2,.9,.2);bolt(27,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(223,13,72,2,.9,.2);bolt(223,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(223,27,72,2,.9,.2);bolt(223,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(237,13,72,2,.9,.2);bolt(237,13,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(237,27,72,2,.9,.2);bolt(237,27,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,98,72,2,.9,.2);bolt(13,98,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(13,112,72,2,.9,.2);bolt(13,112,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,98,72,2,.9,.2);bolt(27,98,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(27,112,72,2,.9,.2);bolt(27,112,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(223,98,72,2,.9,.2);bolt(223,98,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(223,112,72,2,.9,.2);bolt(223,112,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(237,98,72,2,.9,.2);bolt(237,98,72,.8,4,1.3,.55);}
if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {washer(237,112,72,2,.9,.2);bolt(237,112,72,.8,4,1.3,.55);}
}

var canvas = document.getElementById("canvas");
var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

canvas.setAttribute('width', 280);
canvas.setAttribute('height', 280);
canvas.setAttribute('id', 'canvas');
if(typeof G_vmlCanvasManager != 'undefined') {
  canvas = G_vmlCanvasManager.initElement(canvas);
}
ctx = canvas.getContext("2d");
function redraw(){
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  ctx.strokeStyle = "#000000";
  ctx.lineJoin = "round";
  ctx.lineWidth = 6;

  for(var i=0; i < clickX.length; i++) {
    ctx.beginPath();
    if(clickDrag[i] && i){
      ctx.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       ctx.moveTo(clickX[i]-1, clickY[i]);
     }
     ctx.lineTo(clickX[i], clickY[i]);
     ctx.closePath();
     ctx.stroke();
  }
}
function addClick(x, y, dragging)
{
  clickX.push(x);
  clickY.push(y);
  clickDrag.push(dragging);
}
$('#canvas').mousemove(function(e){
  if(paint){
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
    redraw();
  }
});
$('#canvas').mousedown(function(e){
  var mouseX = e.pageX - this.offsetLeft;
  var mouseY = e.pageY - this.offsetTop;

  paint = true;
  addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
  redraw();
});
$('#canvas').mouseup(function(e){
  paint = false;
});
$('#canvas').mouseleave(function(e){
  paint = false;
});
function sendPicture()
{
  sendFileById(ctx);
}

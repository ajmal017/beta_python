var x = 450; //center width
var y = 450; //center height
var _90 = Math.PI/2;
var _180 = Math.PI;
var _360 = Math.PI*2;
var context; //needs to be global
window.onload = setupcontext;

function setupcontext()
{
    //SETUP
    var canvas  = document.getElementById("chart");
    canvas.width = 1800;
    canvas.height = 1800;
    canvas.style.width = "100%";
    canvas.style.height = "100%";
    context = canvas.getContext("2d");
    context.scale(2,2);

    //USERS
    var text = "100.000";
    var users = "USERS";

    var width = context.measureText(text).width;
    var width_users = context.measureText(users).width;
    var height = context.measureText("w").width; // this is a GUESS of height
    context.fillStyle = "#49a52f";
    context.font = "bold 16px verdana, sans-serif";
    context.textAlign = "center";
    context.fillText(text, x ,x - height);
    context.fillText(users, x ,x + height + 10);
    //return fillStyle to black
    context.fillStyle = "black";

    // 1) SMALL GREEN INNER RING
    context.beginPath();
    context.strokeStyle = "#45a018";
    context.lineWidth = 6;
    context.arc(x, y, 53, 0, Math.PI*2); //53 = 50 + lineWidth/2
    context.stroke();

    // THE THREE TERMS
    function rotateCanvas(angle) {

    context.save();
    context.translate(x, x);
    context.rotate(angle);
    context.translate( - x, - x);
    }

    context.font = "16px verdana, sans-serif";

    // drawTextAlongArc(str, radius, angle, charAngle);
    drawTextAlongArc("Needs", 90, _360*33/100, 0.11);
    drawTextAlongArc("Big 5", -100, _360*30/100, -0.1);
    drawTextAlongArc("Values", -100, -_360*48.5/100, -0.1);

    // DATA
    lightBlueInner();
    lightPurpleInner();
    lightGreenInner();
    lightBlueOuter();
    darkBlue();
    darkPurple();
    darkGreen();
}

function lightBlueInner()
{
    context.font = "10px verdana, sans-serif";
    var radius = 110;
    var start = 0;
    var stop = 64;
    var strockStyleOutline = "#5aaafa";
    var strockStyleFill = "#e7f3ff";
    var gap = _180/200;
    var outlineThickness = 1;

    var arrayData = [50];
    var arrayFill = [[94, "Agreeableness"]];

    innerChart(radius, start, stop, strockStyleOutline, strockStyleFill, gap, arrayData, arrayFill,
        outlineThickness);
}

function lightPurpleInner()
{
    context.font = "10px verdana, sans-serif";
    var radius = 110;
    var start = 64;
    var stop = 75;
    var strockStyleOutline = "#ba8ff7";
    var strockStyleFill = "#e7f3ff";
    var gap = _180/200;
    var outlineThickness = 1;

    var arrayData = [50];
    var arrayFill = [[89, "Conservation"]];

    innerChart(radius, start, stop, strockStyleOutline, strockStyleFill, gap, arrayData, arrayFill,
        outlineThickness);
}

function lightGreenInner()
{
    context.font = "10px verdana, sans-serif";
    var radius = 110;
    var start = 75;
    var stop = 100;
    var strockStyleOutline = "#b5e61d";
    var strockStyleFill = "#e7f3ff";
    var gap = _180/200;
    var outlineThickness = 1;

    var arrayData = [50];
    var arrayFill = [[97, "Harmony"]];

    innerChart(radius, start, stop, strockStyleOutline, strockStyleFill, gap, arrayData, arrayFill,
        outlineThickness);
}

function lightBlueOuter()
{
    context.font = "10px verdana, sans-serif";
    var radius = 163;
    var start = 0;
    var stop = 64;
    var strockStyleOutline = "#5aaafa";
    var strockStyleFill = "#e7f3ff";
    var gap = _180/200;
    var outlineThickness = 1;

    var arrayData = [50, 50, 50, 50, 50];
    var arrayFill = [
        [80, "Openness"], [81, "Conscientiousness"], [64, "Extraversion"],
        [94, "Agreeableness"], [50, "Emotional range"]
    ];

    innerChart(radius, start, stop, strockStyleOutline, strockStyleFill, gap, arrayData, arrayFill,
        outlineThickness);
}

function outerTextFont() {context.font = "12px verdana, sans-serif"}

function darkBlue()
{
    outerTextFont();
    var radius = 216;
    var start = 0;
    var stop = 64;
    var strockStyle = "#4178be";
    var gap = _180/400;  

     var arrayData = [
         [90, "Adventurousness"], [98, "Artistic interests"], [99, "Emotionality"],
         [87, "Imagination"], [88, "Intelect"], [65, "Authority-challenginig"],
         [84, "Achievement striving"], [72, "Cautiousness"], [84, "Dutifilulness"],
         [62, "Orderliness"], [83, "Self-discipline"], [70, "Self-efficancy"],
         [89, "Activity level"], [67, "Assertiveness"], [94, "Cheerfulness"],
         [59, "Excitiement-seeking"], [96, "Outgoing"], [66, "Greagariusness"],
         [99, "Altruism"], [86, "Cooperation"], [78,"Modesty"],
         [90, "Uncompromising"], [99, "Sympathy"], [90, "Trust"],
         [17, "Fiery"], [42, "Prone to worry"], [15, "Melancholy"],
         [27, "Immoderation"], [29, "Self-consciousness"], [39, "Susceptible to stress"]
     ];

    outerChart(radius, start, stop, strockStyle, gap, arrayData);
}

function darkPurple()
{
    outerTextFont();
    var radius = 163;
    var start = 64;
    var stop = 75;
    var strockStyle = "#9855d4";
    var gap = _180/400;  

    var arrayData = [
        [89, "Conversation"], [87, "Openness to change"],
        [44, "Hedonism"], [65, "Self-enhancement"], [83, "Self transcedence"]
    ];

    outerChart(radius, start, stop, strockStyle, gap, arrayData);
}

function darkGreen()
{
    outerTextFont();
    var radius = 163;
    var start = 75;
    var stop = 100;
    var strockStyle = "#45a018";
    var gap = _180/400;  

    var arrayData = [
        [67, "Challenge"], [84, "Closeness"], [93, "Curiosity"],
        [74, "Excitement"], [97, "Harmony"], [68, "Ideal"],
        [79, "Liberty"], [82, "Love"], [34, "Practicality"],
        [87, "Self-expression"], [87, "Stabiliy"], [75, "Structure"]
    ];

    outerChart(radius, start, stop, strockStyle, gap, arrayData);
}


//draw functions

function innerChart(
    radius, start, stop, strokeStyleOutline, strokeStyleBackground,
    gap, arrayData, arrayFill, outlineThickness)
{
    var start = _360*start/100 - _90;
    var stop = _360*stop/100 - _90;

    var numberOfElements = arrayData.length;
    var lengthWithGaps = stop - start;
    var lengthWithoutGaps = lengthWithGaps - gap*numberOfElements;
    var elementLength = lengthWithoutGaps/numberOfElements;

    var from = start;
    var to = start + elementLength;

    //VARIABLES FOR TEXT
    var textAngle = _90 + start + elementLength/2;
    var textHorizontal = x;
    context.textAlign = "center";

    for (var i = 0; i < numberOfElements; i++) {
        var size = arrayData[i];

        //draw the outline
        strokeIt(strokeStyleOutline, size, from, to);

        //draw the background
        var from2 = from + _90*outlineThickness/200;
        var to2 = to - _90*outlineThickness/200;
        strokeIt(strokeStyleBackground, (size - outlineThickness*2), from2, to2);

        //draw the data
        strokeIt(strokeStyleOutline, size, from2, from2 + arrayFill[i][0]*(to2 - from2)/100);

        placeTextVertical();
        
        //increment
        textAngle += elementLength + gap;
        from = from + elementLength + gap;
        to = to + elementLength + gap;
    }

    function strokeIt(strokeStyle, sizeFWD, from, to) {
            context.beginPath();
            context.strokeStyle = strokeStyle;
            context.lineWidth = sizeFWD; //forwarded size
            context.arc(x, y, radius + size/2, from, to); //original size
            context.stroke();
     }

    function placeTextVertical() {

        context.save();
        context.translate(x, x);

        var textPossition = textAngle - _90;
        if (textPossition > 0 && textPossition < _180) {
            var finalAngle = textAngle + _180;
            var textHorizontal = - radius - 20;
        } else {
            var finalAngle = textAngle;
            var textHorizontal =  radius + 30;
        }

        var percentHorizontal = textHorizontal - 16;
        context.rotate(finalAngle);
        context.translate( - x, - x);

        var str = arrayFill[i][1];
        var charAngle = 0.040*170/textHorizontal;
        var strAngle = str.length*charAngle;
        drawTextAlongArc(str, textHorizontal, strAngle, charAngle);

        var str = "(" + arrayFill[i][0] + " %)";
        var charAngle = 0.040*170/percentHorizontal;
        var strAngle = str.length*charAngle;
        drawTextAlongArc(str, percentHorizontal, strAngle, charAngle);

        context.restore();
    }
}

function outerChart(radius, start, stop, strockStyle, gap, arrayData) {

    var start=_360*start/100 - _90;
    var stop = _360*stop/100 - _90;

    var numberOfElements = arrayData.length;
    var lengthWithGaps = stop - start;
    var lengthWithoutGaps = lengthWithGaps - gap*numberOfElements;
    var elementLength = lengthWithoutGaps/numberOfElements;
    
    var from = start;
    var to = start + elementLength;

    context.strokeStyle = strockStyle;

    //3 VARIABLES FOR TEXT
    var textAngle = start + elementLength/2;
    var textRadius = radius + 10;
    var textVertical = x + 5;
    context.textAlign = "left";

    for (var i = 0; i <numberOfElements; i++) {
        var size = arrayData[i][0]/2; //normalize to 50/100
        context.beginPath();
        context.lineWidth = size;
        context.arc(x, y, radius + size/2, from, to);
        context.stroke();

        from = from + elementLength + gap;
        to = to + elementLength + gap;

        placeTextHorizontally();
        

        textAngle += elementLength + gap;

    }

    function placeTextHorizontally()
    {
        var angleCorrection = 0.1;
        if (from > _90 + angleCorrection) {
            context.textAlign = "right";
            var finalAngle = textAngle + _180;
            var textHorisontal = x - (textRadius + size);
        } else {
            // context.textAlign = "left";
            var finalAngle = textAngle;
            var textHorisontal = x + (textRadius + size);
        }
        context.save();
        context.translate(x, x);
        context.rotate(finalAngle);
        context.translate( - x, - x);

        context.fillText(arrayData[i][1] + " (" + arrayData[i][0] + " %)", textHorisontal, textVertical);

        context.restore();
    }
}

function drawTextAlongArc(str, radius, angle, charAngle){
    context.save();
    context.translate(x, y);
    context.rotate(-1 * angle / 2);

    for (var n = 0; n < str.length; n++) {
        var char = str[n];

        var charWidth = context.measureText(char).width;
        var charAvgWidth = context.measureText(str).width/str.length;

        context.rotate(charAngle*charWidth/(2*charAvgWidth));
        context.save();

        context.translate(0, -1 * radius);
        
        context.fillText(char, 0, 0);

        context.restore();
        context.rotate(charAngle*charWidth/(2*charAvgWidth));
    }
    context.restore();
}
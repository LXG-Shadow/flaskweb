var keycondition = new Array();
var click = 0;
var clicka = 0;
//循环检测
setInterval(checkkey,10);
//循环cps重置
setInterval(clearcps,1000);

function clearcps()
{
	clicka = click;
	click = 0;
}

//同时检测
function checkkeydown(event)
{
	var evt = event;
	var evtCode = evt.keyCode;
	keycondition[evtCode] = 1;

}

function checkkeyup(event)
{
	var evt = event;
	var evtCode = evt.keyCode;
	keycondition[evtCode] = 0;
}

//检测键盘输入
function checkkey() 
{
	w(keycondition[87]);
	a(keycondition[65]);
	s(keycondition[83]);
	d(keycondition[68]);
}

function w(swither)
{

	var keyc = document.getElementById("w");
	if (swither == 1)
	{
	    keyc.style.backgroundColor = "#C0C0C0" ;
	}
	else
	{
		keyc.style.backgroundColor = "#D3D3D3" ;
	}
}

function a(swither)
{

	var keyc = document.getElementById("a");
	if (swither == 1)
	{
	    keyc.style.backgroundColor = "#C0C0C0" ;
	}
	else
	{
		keyc.style.backgroundColor = "#D3D3D3" ;
	}
}

function s(swither)
{

	var keyc = document.getElementById("s");
	if (swither == 1)
	{
	    keyc.style.backgroundColor = "#C0C0C0" ;
	}
	else
	{
		keyc.style.backgroundColor = "#D3D3D3" ;
	}
}

function d(swither)
{

	var keyc = document.getElementById("d");
	if (swither == 1)
	{
	    keyc.style.backgroundColor = "#C0C0C0" ;
	}
	else
	{
		keyc.style.backgroundColor = "#D3D3D3" ;
	}
}

function cpstestor()
{
	if (click == 0)
	{
		var cps = document.getElementById("cpsvalue");
		cps.innerHTML = clicka + " cps"
		click = click +1;
	}
	else
	{
		click = click +1;
	}
}

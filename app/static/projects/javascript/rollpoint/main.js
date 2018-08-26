var stat = 0;

function gntrad()
{
	var a = parseInt(Math.random()*101);
	document.getElementById("num").innerHTML = a;
}

function sct()
{
	if (stat==0)
	{
		stat = 1;
		stt();
	}
	else if (stat == 1) 
	{
	    stat = 2;
	    stp()	
	}
}

function stt()
{
	gntrad();
	a = setTimeout(stt, 50);
}

function stp()
{
	clearTimeout(a);
	slowdown(50);
}

function slowdown(time)
{
	if (time <=750)
	{
		gntrad();
		a = setTimeout(slowdown,time+100,time+100);
	}
	else
	{
		stat = 0
	}
}
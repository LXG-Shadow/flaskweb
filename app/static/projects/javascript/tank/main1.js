var bulletid = 0;  //子弹id
var barriersid = new Array(); //障碍id：判断是否存在
var barriersidcount = 9; //障碍计数，生成id
var autofire = Boolean();//自动开火状态
var autofiredelay = 650;//自动开火延迟
var tankmovespeedboost = 1;//坦克移速倍数
for (var i=0;i<10;i++) 
{
	barriersid[i] = 1;
}

//检测键盘输入
function checkkey(event) {
	var evt=event;
	var evtCode = evt.keyCode;
	if (evtCode == 37) 
	{
		left();
	}
	if (evtCode == 38) 
	{
		up();
	}
	if (evtCode == 39) 
	{
		right();
	}
	if (evtCode == 40) 
	{
		down();
	}
	if (evtCode == 70)
	{
		gntbullet();
	}
	if (evtCode == 82)
	{
		gntbarriers();
	}
	//if (evtCode == 71) 
	//{
		//systemcommand();
	//}
}

function getClass(obj,name)
{
	if (obj.currentStyle) 
	{
		return obj.currentStyle[name];
	}
	else 
	{
		return getComputedStyle(obj,false)[name];
	}
}

//坦克移动
function up()
{
	var pos = document.getElementById("tank"); //获取坦克img
	var t = pos.style.top; //获取坦克的style里的top的值
	t = parseInt(t.substr(0,t.length-2));//将值转换为数字
	pos.style.top = (t-20*tankmovespeedboost)+"px";//更改top值

}

function down()
{
	var pos = document.getElementById("tank");
	var t = pos.style.top;
	t = parseInt(t.substr(0,t.length-2));
	pos.style.top = (t+20*tankmovespeedboost)+"px";

}

function left()
{
	var pos = document.getElementById("tank");
	var l = pos.style.left;
	l = parseInt(l.substr(0,l.length-2));
	pos.style.left = (l-20*tankmovespeedboost)+"px";
	
}

function right()
{
	var pos = document.getElementById("tank");
	var l = pos.style.left;
	l = parseInt(l.substr(0,l.length-2));
	pos.style.left = (l+20*tankmovespeedboost)+"px";
	
}

//生成子弹
function gntbullet()
{
	bulletid = bulletid + 1 ;//子弹id +1
	var pos = document.getElementById("tank");
	var x = pos.style.left;
	var y = pos.style.top;
	x = parseInt(x.substr(0,x.length-2));
	y = parseInt(y.substr(0,y.length-2));
	x = x+37;
	y = y-28;
	var bulletp = document.getElementById("bulletpaper");//获取子弹div
	var insertImg = document.createElement("img");//创建子img标签
	insertImg.src = "bullet.png";//添加src
	insertImg.className = "bullet";//添加css
	insertImg.style.position = "absolute";
	insertImg.style.left = x + "px";//添加初始位置
	insertImg.style.top = y + "px";//添加初始位置
	insertImg.id = "b" + bulletid;//添加子弹id
	bulletp.appendChild(insertImg);//添加到子弹div
	bulletmv(y,bulletid);//开始自动移动
}

//子弹移动
function bulletmv(y,bulletid)
{
	if (y <= 0) //判断是否到顶
	{
		clearTimeout("a"+bulletid); //取消循环
		var bulletp = document.getElementById("bulletpaper");
		bulletp.removeChild(document.getElementById("b"+bulletid)); //删除子弹
	}
	else
	{
		detecthit(bulletid);
		var bpos = document.getElementById("b"+bulletid);//获取子弹标签
		var y = bpos.style.top;
		//y = parseInt(y.substr(0,y.length-2))-28;
		y = parseInt(y.substr(0,y.length-2))-1;//转化成数字
	    //y = y-28;
	    bpos.style.top = y + "px";//更改位置
        //window["a"+bulletid] = setTimeout(bulletmv,370,y,bulletid);
        window["a"+bulletid] = setTimeout(bulletmv,10,y,bulletid);//循环
	}
}


//检测碰撞
function detecthit(bulletid)
{
	var bpos = document.getElementById("b"+bulletid);
	var x = bpos.style.left;
	var y = bpos.style.top;
	x = parseInt(x.substr(0,x.length-2));
	y = parseInt(y.substr(0,y.length-2));
	for (var i = 0;i<barriersid.length;i++)//依次检测障碍
	{
		if (barriersid[i] == 1)//障碍是否存在
		{
			var bapos = document.getElementById("ba"+i);
			var bax = bapos.style.left;
	        var bay = bapos.style.top;
	        bax = parseInt(bax.substr(0,bax.length-2));
	        bay = parseInt(bay.substr(0,bay.length-2));
	        if (y<bay+40 && x+3>=bax && x+3<=bax+40 && y>bay) //子弹是否碰到障碍
	        {
	        	clearTimeout("a"+bulletid);
	        	var bpos = document.getElementById("b"+bulletid);
	        	bpos.style.top = -40+"px";//更改位置，在bulletmv中取消循环
	        	document.getElementById("ba"+i).src = "barrierhit.png";//障碍被打中后效果
	        	barriersid[i] = 0;//设置此障碍不存在
	        	setTimeout(barrierhit,600,i);//消除障碍
	        }
		}
	}
}

//生成障碍
function gntbarriers()
{
	barriersidcount = barriersidcount + 1;
	barriersid[barriersidcount] = 1
	x = Math.floor((Math.random()*1001));
	y = Math.floor((Math.random()*401));
	var barriersp = document.getElementById("barrierspaper");
	var insertImg = document.createElement("img");
	insertImg.src = "barriers.png";
	insertImg.className = "barriers";
	insertImg.style.position = "absolute";
	insertImg.style.left = x + "px";
	insertImg.style.top = y + "px";
	insertImg.id = "ba" + barriersidcount;
	barriersp.appendChild(insertImg);
}

//消除障碍
function barrierhit(i)
{
	var barriersp = document.getElementById("barrierspaper");
	barriersp.removeChild(document.getElementById("ba"+i));
}

//自动发射子弹
function autogntbullet()
{
	if (autofire)
	{
		gntbullet();
		autof = setTimeout(autogntbullet,autofiredelay);
	}
	else
	{
		clearTimeout(autof);
	}	
}

//摧毁所有障碍
function destoryallbarriers()
{
	for (var i = 0;i<barriersid.length;i++)
	{
		if (barriersid[i] == 1)
		{
			document.getElementById("ba"+i).src = "barrierhit.png";
			barriersid[i] = 0;
		    setTimeout(barrierhit,1000,i);
		}
	}
}


//生成一定量的障碍
function gntcertainamountbarriers(num)
{
	for (var i = 0; i<num ; i++)
	{
		gntbarriers()
	}
}

//命令
function systemcommand()
{
	var command = prompt("Enter The Command","Command");
	if (command != null) 
	{
		command = command.toUpperCase();
		switch(command)
	    {
		    case "DESTORYALLBARRIERS":
		      destoryallbarriers();
	          break;
	        case "AUTOFIRE":
	          autofire = !autofire;
	          autogntbullet();
	          break;
	        case "SETTING":
	          var setting = prompt("Which Setting");
	          if (setting != null) 
	          {
	          	setting = setting.toUpperCase();
	          	switch(setting)
	          	{
	          		case "AUTOFIREDELAY":
	          		  var delay = parseInt(prompt("Enter the delay(in ms)[default:650]:",autofiredelay+""));
	          		  if (delay != null && delay != "" && !isNaN(delay)) 
	          		  {
	          		  	autofiredelay = delay;
	          		  	alert("AutoFireDelay Change Into "+autofiredelay+"ms");
	          		  }
	          		  else
	          		  {
	          		  	alert("Not A Number")
	          		  }
	          		  break;
	          		case "TANKSPEED" :
	          		  var speedfactor = parseFloat(prompt("Enter the multiple of speed:[default: 1]",tankmovespeedboost+""));
	                  if (speedfactor != null && speedfactor != "" && !isNaN(speedfactor))
	                  {
	          	        tankmovespeedboost = speedfactor;
	                  }
	                  else
	                  {
	          	        alert("Not A Number");
	                  }
	                  break;
	          		default :
	          		  alert("No Setting Found");
	          		  break;
	          	}
	          }
	          else 
	          {
	          	alert("You Cancel The Command");
	          }
	          break;
	        case "GENERATEBARRIERS":
	          var num = parseInt(prompt("Enter the number of barriers.","10"));
	          gntcertainamountbarriers(num);
	          break;
	        case "" :
	          alert("No Command Enter");
	          break;
	        default:
	          alert("Command Not Found");
	          break;
	    }
	 }
	else
	{
		alert("You Cancel The Command");
	}
}
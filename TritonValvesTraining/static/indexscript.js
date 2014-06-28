function ajaxRequest()
{
"use strict";
 return new XMLHttpRequest();
}
function SubmitSearch()
{
var ajaxReq = ajaxRequest();
ajaxReq.onreadystatechange = function(){
			if(ajaxReq.readyState === 4 && ajaxReq.status === 200)
			{
				var ifrm = document.getElementById('searchFrame');
				ifrm.innerHTML = ajaxReq.responseText;



			}		
					};
ajaxReq.open("GET", "/viewCart" ,true);
ajaxReq.send();

}
function editEmployee(empid)
{

parent.document.src = '../../editEmp?empID=' + empid ;
}
}
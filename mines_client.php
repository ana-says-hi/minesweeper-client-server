<?php
$s=socket_create(AF_INET,SOCK_STREAM,0);
socket_connect($s,"127.0.0.1",9999);
socket_recv($s,$buf,20,0);
$size=intval($buf);
while($buf!="GAME OVER!BYE!")
{
    $send_me=readline();
    socket_send($s,$send_me,4,0);
    for($i=0;$i<$size+1;$i++)
	{
   	 socket_recv($s,$buf,$size,0);
  	 echo $buf;
	}
}
?>

<!--
ServerSample.asp - an example of Python
and Active Scripting
-->

<%@ Language=Python %>

<%
# Save the URL into a local variable
url = Request.ServerVariables("PATH_INFO")
%>

<H2>Current Document</H2>
The URL to this file is <pre><%= url %></pre><p>
The local path to this URL is <pre><%= Server.MapPath(url) %></pre>

<H2>Client Request Headers</H2>
<% 
for key in Request.ServerVariables:
	Response.Write("%s=%s<br>" % (key, Request.ServerVariables(key)))
%>

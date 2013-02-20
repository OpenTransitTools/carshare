## -*- coding: utf-8 -*- 
<!doctype html>

## BELOW ARE THE ABSTRACT METHODS (to be overridden by sub-classsed templates) that populate this base page
## (sorry they are on one line, but mako puts line breaks in your html, which is ugly)
<%def name="title()">ABSTRACT title()</%def><%def name="app_css()"><!-- ABSTRACT app_css() --></%def><%def name="meta_data()"><!-- ABSTRACT meta_data() --></%def><%def name="header()"><!-- ABSTRACT header() --></%def><%def name="js_onload()">/** ABSTRACT js_onload() **/</%def>
<!--[if lt IE 7]><html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]><html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]><html class="no-js lt-ie9" lang="en"> <![endif]-->
<!-- Consider adding a manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--><html class="no-js" lang="en"><!--<![endif]--><head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="robots" content="all"/>
    ${self.meta_data()}
    <title>${self.title()}</title>

    <link rel="stylesheet" href="/css/common.css"   type="text/css" media="all" />
    ${self.app_css()}
    ${self.header()}
</head>
<body class="standard" onLoad="${self.js_onload()}">
${next.body()}
</body>
</html>

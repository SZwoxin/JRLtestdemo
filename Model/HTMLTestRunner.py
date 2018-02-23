# -*- coding: utf-8 -*-
"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.

The simplest way to use this is to invoke its main method. E.g.

    import unittest
    import HTMLTestRunner

    ... define your tests ...

    if __name__ == '__main__':
        HTMLTestRunner.main()


For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'

    # run the test
    runner.run(my_test_suite)


------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung"
__version__ = "0.8.3"


"""
Change History
Version 0.8.4 by GoverSky
* Add sopport for 3.x
* Add piechart for resultpiechart
* Add Screenshot for selenium_case test
* Add Retry on failed

Version 0.8.3
* Prevent crash on class or module-level exceptions (Darren Wurf).

Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).

Version in 0.8.1
* Validated XHTML (Wolfgang Borgert).
* Added description of test classes and test cases.

Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.

Version in 0.7.1
* Back port to Python 2.3 (Frank Horowitz).
* Fix missing scroll bars in detail log (Podi).
"""

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?
import datetime

import sys
import unittest
from xml.sax import saxutils

PY3K = (sys.version_info[0] > 2)
if PY3K:
    import io as StringIO
else:
    import StringIO
import copy

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging_demo.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging_demo.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

class OutputRedirector ( object ):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write ( s)

    def writelines(self, lines):
        self.fp.writelines ( lines)

    def flush(self):
        self.fp.flush ()


stdout_redirector = OutputRedirector ( sys.stdout )
stderr_redirector = OutputRedirector ( sys.stderr)


# ----------------------------------------------------------------------
# Template

class Template_mixin ( object ):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: u'通过',
        1: u'失败',
        2: u'错误',
    }

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
</head>
<body>
<script language="javascript" type="text/javascript">
output_list = Array();

/* level - 0:Summary; 1:Failed; 2:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level < 1) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level > 1) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
    }
}


function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            document.getElementById('div_'+tid).style.display = 'none'
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

function drawCircle(pass, fail, error){ 
    var color = ["#6c6","#c60","#c00"];  
    var data = [pass,fail,error]; 
    var text_arr = ["pass", "fail", "error"];

    var canvas = document.getElementById("circle");  
    var ctx = canvas.getContext("2d");  
    var startPoint=0;
    var width = 20, height = 10;
    var posX = 112 * 2 + 20, posY = 30;
    var textX = posX + width + 5, textY = posY + 10;
    for(var i=0;i<data.length;i++){  
        ctx.fillStyle = color[i];  
        ctx.beginPath();  
        ctx.moveTo(112,84);   
        ctx.arc(112,84,84,startPoint,startPoint+Math.PI*2*(data[i]/(data[0]+data[1]+data[2])),false);  
        ctx.fill();  
        startPoint += Math.PI*2*(data[i]/(data[0]+data[1]+data[2]));  
        ctx.fillStyle = color[i];  
        ctx.fillRect(posX, posY + 20 * i, width, height);  
        ctx.moveTo(posX, posY + 20 * i);  
        ctx.font = 'bold 14px';
        ctx.fillStyle = color[i];
        var percent = text_arr[i] + ":"+data[i];  
        ctx.fillText(percent, textX, textY + 20 * i);  

    }
}

function show_shots(obj) {
	obj.nextElementSibling.style.display="block";

}

function close_shots(obj) {
	obj.parentElement.style.display="none";	
}

</script>
<div class="piechart">
    <div>
        <canvas id="circle" width="350" height="168" </canvas>
    </div>
</div>
%(heading)s
%(report)s
%(ending)s

</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)


    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
table       { font-size: 100%; }
pre         { }

/* -- heading ---------------------------------------------------------------------- */
h1 {
	font-size: 16pt;
	color: gray;
}
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- css div popup ------------------------------------------------------------------------ */
a.popup_link {
}

a.popup_link:hover {
    color: red;
}
.img{
	width: 50%;
	height: 50%;
	border-collapse: collapse;
    border: 2px solid #777;
}

.screenshots {
    z-index: 100;
	position:absolute;
	left: 20%;
	top: 20%;
	display: none;
}
.close_shots {
	position:absolute;
	top:0; left:48%;
	z-index:99;
	width:20px;
}
.popup_window {
    display: none;
    position: relative;
    left: 0px;
    top: 0px;
    /*border: solid #627173 1px; */
    padding: 10px;
    background-color: #E6E6D6;
    font-family: "Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 8pt;
    width: 500px;
}

}
/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}
#result_table {
    width: 80%;
    border-collapse: collapse;
    border: 1px solid #777;
}
#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}
#result_table td {
    border: 1px solid #777;
    padding: 2px;
}
#total_row  { font-weight: bold; }
.passClass  { background-color: #6c6; }
.failClass  { background-color: #c60; }
.errorClass { background-color: #c00; }
.passCase   { color: #6c6; }
.failCase   { color: #c60; font-weight: bold; }
.errorCase  { color: #c00; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }


/* -- ending ---------------------------------------------------------------------- */
#ending {
}


.piechart{  
    position:absolute;  ;
    top:20px;  
    left:300px; 
    width: 200px;
    float: left;
    display:  inline;
}


</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>

"""  # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
"""  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #

    REPORT_TMPL = """
<p id='show_detail_line'>显示
<a href='javascript:showCase(0)'>概要</a>
<a href='javascript:showCase(1)'>失败</a>
<a href='javascript:showCase(2)'>所有</a>
</p>

<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>测试组/测试用例</td>
    <td>总数</td>
    <td>通过</td>
    <td>失败</td>
    <td>错误</td>
    <td>视图</td>
    <td>错误截图</td>
</tr>
%(test_list)s
<tr id='total_row'>
    <td>统计</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
</tr>
</table>
<script>
    drawCircle(%(Pass)s, %(fail)s, %(error)s)
</script>
"""
    # variables: (test_list, count, Pass, fail, error)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td>%(desc)s</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td><a href="javascript:showClassDetail('%(cid)s',%(count)s)">详情</a></td>
    <td>&nbsp;</td>
</tr>
"""  # variables: (style, desc, count, Pass, fail, error, cid)

    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td ><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <span class='status %(style)s'>
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a></span>

    <div id='div_%(tid)s' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->

    </td>
    <td>%(img)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status,img)

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'><span class='status %(style)s'>%(status)s</span></td>
    <td>%(img)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status,img)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
"""  # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""

    # -------------------- The end of the Template class -------------------

    def __getattribute__(self, item):
        value = object.__getattribute__ ( self, item )
        if PY3K:
            return value
        else:
            if isinstance ( value, str ):
                return value.decode ( "utf-8" )
            else:
                return value


TestResult = unittest.TestResult


class _TestResult ( TestResult ):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1, retry=0):
        TestResult.__init__ ( self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        self.retry = retry
        self.trys = 0
        self.status = 0

    def startTest(self, test):
        TestResult.startTest ( self, test )
        test.img = ""
        self.outputBuffer = StringIO.StringIO ()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue ()

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.

        if self.retry:
            if self.status == 1:
                self.trys += 1
                if self.trys <= self.retry:
                    print("retesting... %d" % self.trys)
                    test = copy.copy ( test )
                    doc = test._testMethodDoc
                    if doc.find ( '_retry' ) != -1:
                        doc = doc[:doc.find ( '_retry' )]
                    desc = "%s_retry:%d" % (doc, self.trys)
                    if not PY3K:
                        if isinstance ( desc, str ):
                            desc = desc.decode ( "utf-8" )
                    test._testMethodDoc = desc
                    test ( self )
                else:
                    self.status = 0
                    self.trys = 0
        self.complete_output ()

    def addSuccess(self, test):
        self.success_count += 1
        self.status = 0
        TestResult.addSuccess ( self, test )
        output = self.complete_output ()
        self.result.append ( (0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write ( 'ok ' )
            sys.stderr.write ( str ( test ) )
            sys.stderr.write ( '\n')
        else:
            sys.stderr.write ( '.')

    def addError(self, test, err):
        self.error_count += 1
        self.status = 1
        TestResult.addError ( self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output ()
        self.result.append ( (2, test, output, _exc_str) )
        try:
            driver = getattr ( test, "driver" )
            test.img = driver.get_screenshot_as_base64 ()
        except AttributeError:
            test.img = ""
        if self.verbosity > 1:
            sys.stderr.write ( 'E  ' )
            sys.stderr.write ( str ( test ) )
            sys.stderr.write ( '\n')
        else:
            sys.stderr.write ( 'E')

    def addFailure(self, test, err):
        self.failure_count += 1
        self.status = 1
        TestResult.addFailure ( self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output ()
        self.result.append ( (1, test, output, _exc_str) )
        try:
            driver = getattr ( test, "driver" )
            test.img = driver.get_screenshot_as_base64 ()
        except AttributeError:
            test.img = ""
        if self.verbosity > 1:
            sys.stderr.write ( 'F  ' )
            sys.stderr.write ( str ( test ) )
            sys.stderr.write ( '\n')
        else:
            sys.stderr.write ( 'F' )


class HTMLTestRunner ( Template_mixin ):
    """
    """

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None, retry=0):
        self.stream = stream
        self.retry = retry
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.datetime.now ()

    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult ( self.verbosity, self.retry )
        test ( result )
        self.stopTime = datetime.datetime.now ()
        self.generateReport ( test, result )
        if PY3K:
            # for python3
            # print('\nTime Elapsed: %s' % (self.stopTime - self.startTime),file=sys.stderr)
            output = '\nTime Elapsed: %s' % (self.stopTime - self.startTime)
            sys.stderr.write ( output )
        else:
            print >> sys.stderr, '\nTime Elapsed: %s' % (self.stopTime - self.startTime)
        return result

    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if not cls in rmap:
                rmap[cls] = []
                classes.append ( cls )
            rmap[cls].append ( (n, t, o, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str ( self.startTime )[:19]
        duration = str ( self.stopTime - self.startTime)
        status = []
        if result.success_count:
            status.append ( u'<span class="tj passCase">Pass</span>%s' % result.success_count )
        if result.failure_count:
            status.append ( u'<span class="tj failCase">Failure</span>%s' % result.failure_count )
        if result.error_count:
            status.append ( u'<span class="tj errorCase">Error</span>%s' % result.error_count)
        if status:
            status = ' '.join ( status)
        else:
            status = 'none'
        return [
            (u'开始时间', startTime),
            (u'耗时', duration),
            (u'状态', status),
        ]

    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes ( result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet ()
        heading = self._generate_heading ( report_attrs )
        report = self._generate_report ( result )
        ending = self._generate_ending ()
        output = self.HTML_TMPL % dict (
            title=saxutils.escape ( self.title ),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
        )
        if PY3K:
            self.stream.write ( output.encode () )
        else:
            self.stream.write ( output.encode ( 'utf8' ))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict (
                name=name,
                value=value,
            )
            a_lines.append ( line )
        heading = self.HEADING_TMPL % dict (
            title=saxutils.escape ( self.title ),
            parameters=''.join ( a_lines ),
            description=saxutils.escape ( self.description ),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult ( result.result )
        for cid, (cls, cls_results) in enumerate ( sortedResult ):
            # subtotal for a class
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                else:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split ( "\n" )[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            row = self.REPORT_CLASS_TMPL % dict(
                style=ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc=desc,
                count=np + nf + ne,
                Pass=np,
                fail=nf,
                error=ne,
                cid='c%s' % (cid + 1),
            )
            rows.append ( row )

            for tid, (n, t, o, e) in enumerate ( cls_results ):
                self._generate_report_test ( rows, cid, tid, n, t, o, e )

        report = self.REPORT_TMPL % dict (
            test_list=u''.join ( rows ),
            count=str ( result.success_count + result.failure_count + result.error_count ),
            Pass=str ( result.success_count ),
            fail=str ( result.failure_count ),
            error=str ( result.error_count ),
        )
        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool ( o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        name = t.id ().split ( '.' )[-1]
        if self.verbosity > 1:
            doc = t.shortDescription () or ""
        else:
            doc = ""

        desc = doc and ('%s: %s' % (name, doc)) or name
        if not PY3K:
            if isinstance ( desc, str ):
                desc = desc.decode ( "utf-8")
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance ( o, str ):
            # uo = unicode(o.encode('string_escape'))
            if PY3K:
                uo = o
            else:
                uo = o.decode ( 'utf-8', 'ignore')
        else:
            uo = o
        if isinstance ( e, str ):
            # ue = unicode(e.encode('string_escape'))
            if PY3K:
                ue = e
            elif e.find ( "AssertionError" ) != -1:
                es = e.decode ( 'utf-8', 'ignore' ).split ( '\n' )
                es[-2] = es[-2].decode ( 'unicode_escape' )
                ue = u"\n".join ( es )
            else:
                ue = e.decode ( 'utf-8', 'ignore')
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=tid,
            output=saxutils.escape ( uo + ue ),
        )
        if t.img:
            img = u"""
            <a href="#" onclick="show_shots(this)">显示截图</a>
            <div class="screenshots">
            <a  class="close_shots" onclick="close_shots(this)">X</a>
            <img src="data:image/jpg;base64,%s" class="img"/>
            </div>""" % t.img
        else:
            img = """"""

        row = tmpl % dict(
            tid=tid,
            Class=(n == 0 and 'hiddenRow' or 'none'),
            style=n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'passCase'),
            desc=desc,
            script=script,
            status=self.STATUS[n],
            img=img,
        )
        rows.append ( row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram ( unittest.TestProgram ):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """

    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner ( verbosity=self.verbosity )
        unittest.TestProgram.runTests ( self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main ( module=None)

from bs4 import BeautifulSoup, NavigableString, Tag
import requests

def html_to_text(html):
    "Creates a formatted text email message as a string from a rendered html template (page)"
    soup = BeautifulSoup(html, 'html.parser')
    # Ignore anything in head
    body, text = soup.body, []
    for element in body.descendants:
        # We use type and not isinstance since comments, cdata, etc are subclasses that we don't want
        if type(element) == NavigableString:
            parent_tags = (t for t in element.parents if type(t) == Tag)
            hidden = False
            for parent_tag in parent_tags:
                # Ignore any text inside a non-displayed tag
                # We also behave is if scripting is enabled (noscript is ignored)
                # The list of non-displayed tags and attributes from the W3C specs:
                if (parent_tag.name in ('area', 'base', 'basefont', 'datalist', 'head', 'link',
                                        'meta', 'noembed', 'noframes', 'param', 'rp', 'script',
                                        'source', 'style', 'template', 'track', 'title', 'noscript') or
                    parent_tag.has_attr('hidden') or
                    (parent_tag.name == 'input' and parent_tag.get('type') == 'hidden')):
                    hidden = True
                    break
            if hidden:
                continue

            # remove any multiple and leading/trailing whitespace
            string = ' '.join(element.string.split())
            if string:
                if element.parent.name == 'a':
                    a_tag = element.parent
                    # replace link text with the link
                    string = a_tag['href']
                    # concatenate with any non-empty immediately previous string
                    if (    type(a_tag.previous_sibling) == NavigableString and
                            a_tag.previous_sibling.string.strip() ):
                        text[-1] = text[-1] + ' ' + string
                        continue
                elif element.previous_sibling and element.previous_sibling.name == 'a':
                    text[-1] = text[-1] + ' ' + string
                    continue
                elif element.parent.name == 'p':
                    # Add extra paragraph formatting newline
                    string = '\n' + string
                text += [string]
    doc = '\n'.join(text)
    return doc

if __name__ == '__main__':
    html = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Hello World!</title>
    </head>
    <body style="margin:0; padding:0; background-color:#F2F2F2;">
        <!--[if !mso]><!-- -->
        <img style="min-width:640px; display:block; margin:0; padding:0" class="mobileOff" width="640" height="1" src="/static/spacer.gif">
        <!--<![endif]-->

        <center>
            <table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#F2F2F2">
                <tr>
                    <td align="center" class="mobile" style="font-family:arial, sans-serif; font-size:20px; line-height:26px; font-weight:bold;">
                        This is some title text.
                    </td>
                </tr>
                <script>This is a script</script>
                <tr>
                    <td align="center" class="mobile" style="font-family:arial, sans-serif; font-size:20px; line-height:26px; font-weight:bold;">
                        <p>   Paragraph without 
                        
                        link    <br>  But with a 
                        
                        line break  </p>
                    </td>
                </tr>
                <tr>
                    <td align="center" class="mobile" style="font-family:arial, sans-serif; font-size:20px; line-height:26px; font-weight:bold;">
                        <a href="http://www.dummy-domain.co.wibble/button-link/">This is a button link &gt;</a>
                    </td>
                </tr>
                <style type="text/css">
                  /* CLIENT-SPECIFIC STYLES */
                body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
                table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
                img { -ms-interpolation-mode: bicubic; }
                </style>
                <script>This is a longer script with embedded tags:
                    '<p>Example embedded tag with <i class="fa fa-example">icon</i></p>'
                </script>
                <p hidden>Non-visible paragraph with <i class="fa fa-example">icon</i></p>
                <noscript>This is a longer script with embedded tags:
                    <p>Example embedded text with <i class="fa fa-example">icon</i></p>
                </noscript>
                <form>
                <input id="id_wibble" class="form-control" name="wibble" type="hidden" placeholder="Something here">
                <input id="id_email" class="form-control" name="email" type="email" placeholder="Your email address">
                </form>
                <tr>
                    <td align="center" class="mobile" style="font-family:arial, sans-serif; font-size:20px; line-height:26px; font-weight:bold;">
                        <p>Paragraph with embedded link <a href="http://www.dummy-domain.co.wibble/paragraph-link/">This is a link &gt;</a>
                        and this is a continuation of the paragraph with the link.</p>
                    </td>
                </tr>
                <tr>
                    <td align="center" class="mobile" style="font-family:arial, sans-serif; font-size:20px; line-height:26px; font-weight:bold;">
                        Some text with link: <a href="http://www.dummy-domain.co.wibble/text-link/">This is a link &gt;</a>
                        And some text after the link.<br>
                        Try an empty embedded link<a href="">This is a link &gt;</a>before this text.<br>
                        Lots of brs:<br><br><br>
                        after brs
                    </td>
                </tr>
            </table>
        </center>
    </body>
    </html>
    """
    print(html_to_text(html))
    print('\n\n\nNEWS ARTICLE\n\n')
    url = 'https://arstechnica.com/?p=1678422'
    r = requests.get(url)
    if r.status_code == 200:
        print(html_to_text(r.text))

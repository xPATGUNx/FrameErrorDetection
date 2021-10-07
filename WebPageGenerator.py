from airium import Airium
from airium import from_html_to_airium
import json
import glob
import os


# TODO: Add Pydoc
def create_html_report_from_python(*, title_of_test_run: str,
                                   amount_of_frame_errors: int,
                                   amount_of_frame_drops: int,
                                   path_to_video: str,
                                   dict_of_frame_errors: dict,
                                   list_of_frame_error_distances: list,
                                   list_of_scan_results: list,
                                   expected_amount_of_frames: int):
    a = Airium()

    a('<!DOCTYPE html>')
    with a.html(lang='en'):
        with a.head():
            a.meta(charset='UTF-8')
            a.title(_t=title_of_test_run)
            with a.style():
                a('html *\n'
                  '{\n'
                  'color: dimgrey;\n'
                  'font-family: Courier,serif !important;\n'
                  '}\n'
                  'h3 {\n'
                  'font-size: 100%;\n'
                  '}\n'
                  'hr {\n'
                  'border-top: 1px dashed grey;\n'
                  '}\n'
                  'img {\n'
                  'width: 100%;\n'
                  'margin-left: -10%;\n'
                  '}\n'
                  '.dataCell{\n'
                  'vertical-align: top;\n'
                  '}\n'
                  '.headline {\n'
                  'background-color: cornflowerblue;\n'
                  '}')
        with a.body():
            with a.div(klass='headline'):
                a.h1(style='color: aliceblue; margin-left: 1%', _t=title_of_test_run)
                a.hr()
            with a.div(klass='stats', style='font-size: larger'):
                with a.table(style='width: 100%; font-size: x-large'):
                    with a.tr():
                        if amount_of_frame_errors != 0:
                            a.td(_t=f'&#10071 Total amount of frame errors: {amount_of_frame_errors}')
                            a.td(_t=f'&#10060 Amount of dropped frames: {amount_of_frame_drops}')
                            a.td(_t=f'&#127909 Expected amount of frames: {expected_amount_of_frames}')
                        else:
                            a.td(_t=f'&#9989 Total amount of frame errors: {amount_of_frame_errors}')
                            a.td(_t=f'&#9989 Amount of dropped frames: {amount_of_frame_drops}')
                            a.td(_t=f'&#127909 Expected amount of frames: {expected_amount_of_frames}')
                a.hr()
            with a.div(klass='visual'):
                with a.table(style='width: 100%'):
                    with a.tr():
                        a.td(_t='Graph of frame occurrences:')
                        a.td(_t='Display stats:')
                    with a.tr():
                        with a.td():
                            a.img(alt='Occurrence Graph', src="Data/Occurrence%20Graph.png")
                        with a.td():
                            a.img(alt='Frame Stats', src="Data/Frame%20Stats.png")
                a.hr()
            with a.div(klass='dataDisplay', style='width: 100%; height: 250px; resize: vertical; overflow: auto'):
                with a.table():
                    with a.tr():
                        with a.td(klass='dataCell'):
                            with a.table():
                                with a.tr():
                                    a.th(_t='Detected Frame Errors:')
                                with a.tr():
                                    with a.td():
                                        with a.ul():
                                            if len(dict_of_frame_errors) != 0:
                                                for key, value in dict_of_frame_errors.items():
                                                    a.li(_t=f'Frame {key} occurred {value[0]} times. '
                                                            f'Time Code position: {value[1]}.')
                                            else:
                                                a.li(_t=f'No Frame Errors detected.')
                        with a.td(klass='dataCell'):
                            with a.table():
                                with a.tr():
                                    a.th(_t='Distances between frame errors:')
                                with a.tr():
                                    with a.td():
                                        with a.ul():
                                            if list_of_frame_error_distances is not None:
                                                for distance_of_error in list_of_frame_error_distances:
                                                    a.li(_t=f'{distance_of_error}')
                                            else:
                                                a.li(_t=f'')
                        with a.td(klass='dataCell'):
                            with a.table():
                                with a.tr():
                                    a.th(_t='Detected frames:')
                                with a.tr():
                                    with a.td():
                                        with a.ul():
                                            if list_of_frame_error_distances is not None:
                                                for scan_result in list_of_scan_results:
                                                    a.li(_t=f'{scan_result}')
                                            else:
                                                a.li(_t=f'')
            with a.div(klass='video'):
                a.hr()
                a.p(_t='Recording footage:')
                with a.video(controls='', width='100%'):
                    a.source(src=f'Data/{path_to_video}')
                    a('Your browser does not support HTML video.')

    html = str(a)  # casting to string extracts the value

    return html


# TODO: Add Pydoc
def read_json_file(path_to_file):
    with open(path_to_file, 'r') as json_reader:
        json_file = json_reader.read()
        content = json.loads(json_file)
        return content


# TODO: Add Pydoc
def generate_html_report(report_dir: str, data_dir: str):
    json_file = '*.json'
    path_to_json = os.path.join(data_dir, json_file)
    for file in glob.glob(path_to_json):
        json_file = file
    test_data = read_json_file(json_file)

    video_file = ''
    video_file_dir = '*.mp4'
    path_to_recording = os.path.join(data_dir, video_file_dir)
    for file in glob.glob(path_to_recording):
        video_file = file
    path_to_video = os.path.basename(video_file)

    report_title = test_data['title']
    amount_of_errors = test_data['total amount of frame errors']
    amount_of_drops = test_data['total amount of frame drops']
    expected_amount_of_frames = test_data['expected amount of frames']
    frame_error_dict = test_data['detected frame errors']
    distances_list = test_data['distances between frame errors']
    scan_results_list = test_data['scan results']

    html = create_html_report_from_python(title_of_test_run=report_title,
                                          amount_of_frame_errors=amount_of_errors,
                                          amount_of_frame_drops=amount_of_drops,
                                          expected_amount_of_frames=expected_amount_of_frames,
                                          path_to_video=path_to_video,
                                          dict_of_frame_errors=frame_error_dict,
                                          list_of_frame_error_distances=distances_list,
                                          list_of_scan_results=scan_results_list)

    report_root = 'Reports'
    report_data_dir = report_dir
    html_report_file_name = 'Report.html'
    html_report_path = os.path.join(report_root, report_data_dir, html_report_file_name)
    try:
        with open(html_report_path, 'w') as html_writer:
            for lines in html:
                html_writer.write(lines)
    finally:
        html_writer.close()


def test_py_to_html():
    a = Airium()

    a('<!DOCTYPE html>')
    with a.html(lang='en'):
        with a.head():
            a.meta(charset='UTF-8')
            a.title(_t='Frame Error Test Report Example')
            with a.style():
                a('html *\n'
                  '{\n'
                  'color: dimgrey;\n'
                  'font-family: Courier,serif !important;\n'
                  '}\n'
                  'h3 {\n'
                  'font-size: 100%;\n'
                  '}\n'
                  'hr {\n'
                  'border-top: 1px dashed grey;\n'
                  '}\n'
                  'img {\n'
                  'width: 100%;\n'
                  'margin-left: -10%;\n'
                  '}\n'
                  '.dataCell{\n'
                  'vertical-align: top;\n'
                  '}\n'
                  '.headline {\n'
                  'background-color: cornflowerblue;\n'
                  '}')
        with a.body():
            with a.div(klass='headline'):
                a.h1(style='color: aliceblue; margin-left: 1%', _t='Frame Error Test Report Example')
                a.hr()
            with a.div(klass='stats', style='font-size: larger'):
                with a.table(style='width: 60%; font-size: x-large'):
                    with a.tr():
                        a.td(_t='❗ Total amount of frame errors: 3')
                        a.td(_t='❌ Amount of dropped frames: 1')
                a.hr()
            with a.div(klass='visual'):
                with a.table(style='width: 100%'):
                    with a.tr():
                        a.td(_t='Graph of frame occurrences:')
                        a.td(_t='Display stats:')
                    with a.tr():
                        with a.td():
                            a.img(alt='Occurrence Graph', src='Data/Occurrence%20Graph%202021-09-21%2010-56-18.mp4.png')
                        with a.td():
                            a.img(alt='Frame Stats', src='Data/Frame%20Stats%202021-09-21%2010-56-18.mp4.png')
                a.hr()
            with a.div(klass='dataDisplay', style='width: 100%; height: 250px; resize: vertical; overflow: auto'):
                with a.table():
                    with a.tr():
                        with a.td(klass='dataCell'):
                            with a.table():
                                with a.tr():
                                    a.th(_t='Detected Frame Errors:')
                                with a.tr():
                                    with a.td():
                                        with a.ul():
                                            for i in range(5):
                                                a.li(_t='Frame 4376 occurred 2 times. Time Code position: 0:1:12:916')
                        with a.td(klass='dataCell'):
                            with a.table():
                                with a.tr():
                                    a.th(_t='Distances between frame errors:')
                                with a.tr():
                                    with a.td():
                                        with a.ul():
                                            a.li(_t='Distance between frame error 4376 and 4378: 2')
                                            a.li(_t='Distance between frame error 4376 and 4378: 2')
                                            a.li(_t='Distance between frame error 4376 and 4378: 2')
                                            a.li(_t='Distance between frame error 4376 and 4378: 2')
                                            a.li(_t='Distance between frame error 4376 and 4378: 2')
                        with a.td(klass='dataCell'):
                            with a.table():
                                with a.tr():
                                    a.th(_t='Detected frames:')
                                with a.tr():
                                    with a.td():
                                        with a.ul():
                                            a.li(_t='Frame 1 occurred 1 times.')
                                            a.li(_t='Frame 2 occurred 1 times.')
                                            a.li(_t='Frame 3 occurred 1 times.')
                                            a.li(_t='Frame 4 occurred 1 times.')
                                            a.li(_t='Frame 5 occurred 1 times.')
                                            a.li(_t='Frame 6 occurred 1 times.')
                                            a.li(_t='Frame 7 occurred 1 times.')
                                            a.li(_t='Frame 8 occurred 1 times.')
                                            a.li(_t='Frame 9 occurred 1 times.')
                                            a.li(_t='Frame 10 occurred 1 times.')
                                            a.li(_t='Frame 11 occurred 1 times.')
                                            a.li(_t='Frame 12 occurred 1 times.')
                                            a.li(_t='Frame 13 occurred 1 times.')
                                            a.li(_t='Frame 14 occurred 1 times.')
                                            a.li(_t='Frame 15 occurred 1 times.')
                                            a.li(_t='Frame 16 occurred 1 times.')
                                            a.li(_t='Frame 17 occurred 1 times.')
                                            a.li(_t='Frame 18 occurred 1 times.')
                                            a.li(_t='Frame 19 occurred 1 times.')
                                            a.li(_t='Frame 20 occurred 1 times.')
            with a.div(klass='video'):
                a.hr()
                a.p(_t='Recording footage:')
                with a.video(controls='', width='100%'):
                    a.source(src='Data/2021-09-21 10-56-18.mp4', type='video/mp4')
                    a('Your browser does not support HTML video.')

    html = str(a)  # casting to string extracts the value

    print(html)


def test_html_to_py():
    # assume we have such a page given as a string:
    html_str = """\
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Frame Error Test Report Example</title>
        <style>
            html *
                {
                   color: dimgrey;
                   font-family: Courier,serif !important;
                }
            h3 {
                font-size: 100%;
            }
            hr {
                border-top: 1px dashed grey;
            }
            img {
               width: 100%;
               margin-left: -10%;
            }
            .dataCell{
                vertical-align: top;
            }
            .headline {
                background-color: cornflowerblue;
            }
        </style>
    </head>
    
    <body>
        <div class="headline">
            <h1 style="color: aliceblue; margin-left: 1%">Frame Error Test Report Example</h1>
            <hr>
        </div>
    
        <div class="stats" style="font-size: larger">
            <table style="width: 60%; font-size: x-large">
                <tr>
                    <td>&#10071; Total amount of frame errors: 3</td>
                    <td>&#10060; Amount of dropped frames: 1</td>
                </tr>
            </table>
            <hr>
        </div>
    
        <div class="visual">
            <table style="width: 100%">
                <tr>
                    <td>Graph of frame occurrences:</td>
                    <td>Display stats:</td>
                </tr>
                <tr>
                    <td><img src="Data/Occurrence%20Graph%202021-09-21%2010-56-18.mp4.png" alt="Occurrence Graph"></td>
                    <td><img src="Data/Frame%20Stats%202021-09-21%2010-56-18.mp4.png" alt="Frame Stats"></td>
                </tr>
            </table>
            <hr>
        </div>
    
        <div class="dataDisplay" style="width: 100%; height: 250px; resize: vertical; overflow: auto">
            <table>
                <tr>
                    <td class="dataCell">
                        <table>
                            <tr>
                                <th>Detected Frame Errors:</th>
                            </tr>
                            <tr>
                                <td>
                                    <ul>
                                        <li>Frame 4376 occurred 2 times. Time Code position: 0:1:12:916</li>
                                        <li>Frame 4376 occurred 2 times. Time Code position: 0:1:12:916</li>
                                        <li>Frame 4376 occurred 2 times. Time Code position: 0:1:12:916</li>
                                        <li>Frame 4376 occurred 2 times. Time Code position: 0:1:12:916</li>
                                        <li>Frame 4376 occurred 2 times. Time Code position: 0:1:12:916</li>
                                    </ul>
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td class="dataCell">
                        <table>
                            <tr>
                                <th>Distances between frame errors:</th>
                            </tr>
                            <tr>
                                <td>
                                    <ul>
                                        <li>Distance between frame error 4376 and 4378: 2</li>
                                        <li>Distance between frame error 4376 and 4378: 2</li>
                                        <li>Distance between frame error 4376 and 4378: 2</li>
                                        <li>Distance between frame error 4376 and 4378: 2</li>
                                        <li>Distance between frame error 4376 and 4378: 2</li>
                                    </ul>
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td class="dataCell">
                        <table>
                            <tr>
                                <th>Detected frames:</th>
                            </tr>
                            <tr>
                                <td>
                                    <ul>
                                        <li>Frame 1 occurred 1 times.</li>
                                        <li>Frame 2 occurred 1 times.</li>
                                        <li>Frame 3 occurred 1 times.</li>
                                        <li>Frame 4 occurred 1 times.</li>
                                        <li>Frame 5 occurred 1 times.</li>
                                        <li>Frame 6 occurred 1 times.</li>
                                        <li>Frame 7 occurred 1 times.</li>
                                        <li>Frame 8 occurred 1 times.</li>
                                        <li>Frame 9 occurred 1 times.</li>
                                        <li>Frame 10 occurred 1 times.</li>
                                        <li>Frame 11 occurred 1 times.</li>
                                        <li>Frame 12 occurred 1 times.</li>
                                        <li>Frame 13 occurred 1 times.</li>
                                        <li>Frame 14 occurred 1 times.</li>
                                        <li>Frame 15 occurred 1 times.</li>
                                        <li>Frame 16 occurred 1 times.</li>
                                        <li>Frame 17 occurred 1 times.</li>
                                        <li>Frame 18 occurred 1 times.</li>
                                        <li>Frame 19 occurred 1 times.</li>
                                        <li>Frame 20 occurred 1 times.</li>
                                    </ul>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>
    
        <div class="video">
            <hr>
            <p>Recording footage:</p>
            <video width="100%" controls>
            <source src="Data/2021-09-21 10-56-18.mp4" type="video/mp4">
            Your browser does not support HTML video.
            </video>
        </div>
    </body>
    </html>
    """

    # to convert the html into python, just call:

    py_str = from_html_to_airium(html_str)
    print(py_str)


# test_html_to_py()
# test_py_to_html()

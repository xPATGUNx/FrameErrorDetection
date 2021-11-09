from airium import Airium
from airium import from_html_to_airium
import json
import glob
import os
import webbrowser


def create_html_report_from_python(*, title_of_test_run: str,
                                   amount_of_frame_errors: int,
                                   amount_of_frame_drops: int,
                                   path_to_video: str,
                                   dict_of_frame_errors: dict,
                                   list_of_frame_error_distances: list,
                                   list_of_scan_results: list,
                                   expected_amount_of_frames: int):
    """
    Creates an HTML string based on the given parameters by using Airium.
    :param title_of_test_run: A string of the test run / report title.
    :param amount_of_frame_errors: An integer of the total amount of occurred frame errors.
    :param amount_of_frame_drops: An integer of the total amount of occurred frame drops.
    :param path_to_video: A string of the path to the recorded video.
    :param dict_of_frame_errors: A dictionary containing every frame error index.
    :param list_of_frame_error_distances: A list containing the distances between frame errors.
    :param list_of_scan_results: A list containing all scanned frames.
    :param expected_amount_of_frames: An integer of the total amount of expected frames.
    :return: Returns an HTML string filled with the report content.
    """
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


def read_json_file(path_to_file):
    """
    Reads and loads content of a json file.
    :param path_to_file: String of json file path.
    :return: Returns content of json file.
    """
    with open(path_to_file, 'r') as json_reader:
        json_file = json_reader.read()
        content = json.loads(json_file)
        return content


def generate_html_report(report_dir: str, data_dir: str, open_report: bool):
    """
    Generates the report and stores it in an HTML file.
    :param report_dir: Path string to the directory of the report save location.
    :param data_dir: Path string of the data storage directory.
    :param open_report: A boolean that opens the report after the test run if set true.
    """
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

    report_data_dir = report_dir
    html_report_file_name = 'Report.html'
    html_report_path = os.path.join(report_data_dir, html_report_file_name)
    try:
        with open(html_report_path, 'w') as html_writer:
            for lines in html:
                html_writer.write(lines)
    finally:
        if open_report is True:
            webbrowser.open('file://' + os.path.realpath(html_report_path))
        html_writer.close()

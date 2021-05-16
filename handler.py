from github import releases


def download_rct2(working_folder, builder):
    download_view_container = builder.get_object("DownloadContainer")
    download_label = builder.get_object("LblSpeed")
    progress_bar = builder.get_object("PgrDownload")

    # UI Updates
    download_view_container.set_no_show_all(False)
    download_view_container.show_all()
    download_label.set_text("Getting latest release...")

    manager = releases.ReleaseManager("OpenRCT2", "OpenRCT2", builder)

    selected_url, selected_filename = manager.get_asset_download_url_and_name()
    if selected_url is None and selected_filename is None:
        download_label.set_text("Connection error. Please try again.")
        return

    return_data = manager.download_asset(working_folder, selected_url, selected_filename, progress_bar)

    if return_data != 0:
        download_label.set_text(return_data)

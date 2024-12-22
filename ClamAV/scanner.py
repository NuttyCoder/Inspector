import pyclamd

def scan_file(file_path):
    cd = pyclamd.ClamdAgnostic()
    
    # Check if ClamAV daemon is running
    if not cd.ping():
        raise Exception("ClamAV daemon is not running")
    
    scan_result = cd.scan_file(file_path)
    
    if scan_result is None:
        return "No virus found."
    else:
        return scan_result

def scan_directory(directory_path):
    cd = pyclamd.ClamdAgnostic()
    
    # Check if ClamAV daemon is running
    if not cd.ping():
        raise Exception("ClamAV daemon is not running")
    
    scan_result = cd.scan_directory(directory_path)
    
    if scan_result is None:
        return "No virus found in the directory."
    else:
        return scan_result

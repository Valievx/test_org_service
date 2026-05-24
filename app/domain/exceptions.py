class AppError(Exception):
    status_code = 400
    message = "Application Error"


class ParentNotFoundError(AppError):
    status_code = 404
    message = "Parent Not Found"


class DepartmentAlreadyExistsError(AppError):
    status_code = 400
    message = "Department with this name already exists"


class DepartmentNotFoundError(AppError):
    status_code = 404
    message = "Department not found"


class DepartmentCycleError(AppError):
    status_code = 400
    message = "Department cycle error"


class InvalidReassignError(AppError):
    status_code = 400
    message = "Invalid reassign parameter"
from deta import Deta

deta = Deta()

databases = {
    "users": deta.Base("users"),
    "stats": deta.Base("stats")
}


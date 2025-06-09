{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.redis
    pkgs.gunicorn
  ];
  env = {
    PYTHONPATH = ".";
  };
}

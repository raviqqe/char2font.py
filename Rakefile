VENV_DIR = '.venv'


def vsh *args
  sh ". #{VENV_DIR}/bin/activate && #{args.join ' '}"
end


task :test => :clean do
  sh "python3 -m venv #{VENV_DIR}"
  vsh 'python setup.py install'
  sh 'wget http://font.sumomo.ne.jp/fontdata-c2157415/k-font.zip'
  sh 'unzip *.zip'
  vsh 'char2font -f keifont.ttf data/foo.txt'
end


task :upload => :test do
    sh 'python3 setup.py sdist bdist_wheel'
    sh 'twine upload dist/*'
end


task :clean do
  sh 'git clean -dfx'
end

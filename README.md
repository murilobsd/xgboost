## Compilando

```
git clone --recursive https://github.com/murilobsd/xgboost
cd xgboost
mkdir build
cd build
cmake
make -j4
```

## Testando ambientes

Será criado a biblioteca na pasta lib/, como essa biblioteca não tem
nenhuma otimização como GPU, OPENSMP, faremos uma copia da mesma para
simular a versão do xgboost em python e em cython, para isso digite
os comandos abaixo:

```
# isso pode variar de acordo com o sistema operacional
# por exemplo no windows pode ser lib/xgboost.dll

cp lib/libxgboost.so lib/libcythonize_xgboost.so

# Abra outro terminal e crie um ambiente virtual
# fora da pasta do projeto (pasta clonada) isso porque
# iremos acessar uma outra branch o que pode destruir seu
# ambiente virtual.
mkdir -p ~/src/python
cd ~/src/python
python3 -m venv venv # criamos um ambiente virtual
```

### Python puro

Acesse a pasta python-packages do projeto e ative ambiente virtual
criado anteriormente

```
cd python-packages/
. ~/src/python/venv/bin/activate # isso pode variar de SO para SO
python setup.py install
```

Testando:

Quando passamos nenhum argumento a esse script ele usa a versão original do 
xgboost

```
./test_benchmark.py
```

### Cython

Baixa as branches remotas, acesse a branch **cythonize** depois acesse a 
pasta python-packages do projeto e ative ambiente virtual criado anteriormente

```
git fetch -a
git checkout cythonize
cd python-packages/
. ~/src/python/venv/bin/activate # isso pode variar de SO para SO
python setup.py build_ext --inplace
python setup.py install
```

Agora iremos fazer o processo manualmente no futuro será feito um script
para isso. Nós iremos copiar alguns arquivos para dentro de nosso ambiente
virtual para criar o pacote final chamado **cythonize_xgboost**.

```
cp cythonize_xgboost/config.py ~/src/python/venv/lib/python3.9/site-packages/cythonize_xgboost/
cp cythonize_xgboost/VERSION ~/src/python/venv/lib/python3.9/site-packages/cythonize_xgboost/
mkdir ~/src/python/venv/lib/python3.9/site-packages/cythonize_xgboost/lib
cp ../lib/libcythonize_xgboost.so ~/src/python/venv/lib/python3.9/site-packages/cythonize_xgboost/lib
```

Testando:

Quando passamos nenhum argumento a esse script ele usa a versão original do 
xgboost

```
./test_benchmark.py "cythonize"
```

Eu recomendo o uso do [hyperfine](https://github.com/sharkdp/hyperfine) para gerar o benchmark, o software é específico para isso com
inúmeras features. Por exemplo poderia ser usado da seguinte forma

```
hyperfine --warmup 5 "./test_bench.py" "./test_bench.py 'cythonize'"
```

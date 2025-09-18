from typing import List
from setuptools import find_packages,setup


requirement_lst:list[str]
def get_requirements()->list[str]:
    requirement_lst:list[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line  in lines:
                requirement=line.strip()
                if requirement and requirement != ' -e .':
                   requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirement.txt not found")

    return requirement_lst

print(get_requirements())

setup(
    name="Networksecurity",
    version="0.0.1",
    author="ibrahim",
    author_email="ibrahimwasim.1202@gmail.com",
    packages=find_packages(),
    install_req=get_requirements()
)
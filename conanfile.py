#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class QuantLibConan(ConanFile):
    name = "QuantLib"
    version = "1.12.0"
    url = "https://github.com/lballabio/QuantLib"
    description = "A free/open-source library for quantitative finance"
    license = "https://github.com/lballabio/QuantLib/blob/master/LICENSE.TXT"
    exports_sources = ["CMakeLists.txt", "LICENSE.TXT", "cmake/*", "Examples/*", "ql/*", "test-suite/*",]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], 
               "USE_BOOST_DYNAMIC_LIBRARIES": [True, False]}
    default_options = "shared=False", "USE_BOOST_DYNAMIC_LIBRARIES=True"
    requires = "Boost/1.64.0@conan/stable",
    generators = "cmake"

    def source(self):
        # This should be in CMakeLists.txt, but do not want to be intrusive right now
        tools.replace_in_file("./CMakeLists.txt", "project(QuantLib)", 
        '''project(QuantLib)
           include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
           conan_basic_setup()
        ''')

    def build(self):
        cmake = CMake(self)
        if self.options["USE_BOOST_DYNAMIC_LIBRARIES"]:
            cmake.definitions["USE_BOOST_DYNAMIC_LIBRARIES"] = True
        cmake.configure(source_dir=".")
        cmake.build()

    def package(self):
        with tools.chdir("."):
            self.copy(pattern="LICENSE")
            self.copy(pattern="*", dst="include", src="include")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

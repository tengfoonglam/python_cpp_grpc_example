#! /usr/bin/env python

import pkg_resources
import copy

from setuptools import setup
from setuptools import Command
from setuptools.command.install import install
from setuptools.command.develop import develop

# List of all .proto files
proto_srcs = [
    'arithmetic_proto/average.proto', 'arithmetic_proto/max.proto', 'arithmetic_proto/prime.proto',
    'arithmetic_proto/sum.proto'
]

# List of paths where we can find the .proto files from other modules you have used
import_paths = ['.']

# Note what we are doing here. We create a custom command CompileProtos and register it in setuptools.setup as 'compile_protos'
# We then override the default install and develop commands
# install is called when you run pip install . --> No pb2.py and pb2_grpc.py files will be generated in the source directory
# deveop is called when you run pip install -e . --> pb2.py and pb2_grpc.py will be generated in the source directory


class InstallCommand(install):
    def run(self):
        self.run_command("compile_protos")
        return super().run()


class DevelopCommand(develop):
    def run(self):
        self.run_command("compile_protos")
        return super().run()


class CompileProtos(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.protoc

        def generate_proto(source, import_paths):
            proto_import = pkg_resources.resource_filename('grpc_tools', '_proto')
            import_paths_complete = copy.deepcopy(import_paths)
            import_paths_complete.append(proto_import)

            import_path_commands = []
            for import_path in import_paths_complete:
                import_path_commands.append(f"-I{import_path}")
            import_path_commands

            command_arguments = ['grpc_tools.protoc']
            command_arguments += import_path_commands
            command_arguments += ['--python_out=.', '--grpc_python_out=.']
            command_arguments += [source]

            grpc_tools.protoc.main(command_arguments)

        print("[CompileProtos] Compiling proto files...")
        for proto_src in proto_srcs:
            print(f"[CompileProtos] Processing proto file {proto_src}")
            generate_proto(proto_src, import_paths)


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(name='arithmetic_proto',
      packages=["arithmetic_proto"],
      install_requires=["grpcio>=1.47.0", "grpcio-tools>=1.47.0", "protobuf>=3.19"],
      author='Lam Teng Foong',
      author_email='tengfoonglam@yahoo.com.sg',
      description='Python package from arithmetic proto files',
      long_description="",
      cmdclass={
          'compile_protos': CompileProtos,
          'develop': DevelopCommand,
          'install': InstallCommand
      },
      python_requires=">=3.6")

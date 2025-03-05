# /di/container.py
import importlib
import pkgutil


class DependencyContainer:
    def __init__(self):
        self.dependencies = {}
        self._register_dependencies()

    def _import_modules_from_package(self, package_name):
        """Belirtilen paketteki tüm modülleri yükler."""
        package = importlib.import_module(package_name)
        return {
            name: importlib.import_module(f"{package_name}.{name}")
            for _, name, _ in pkgutil.iter_modules(package.__path__)
        }

    def _register_dependencies(self):
        """Data Access, Services ve Helpers klasörlerini tarar ve tüm sınıfları container'a ekler."""
        modules = {}
        modules.update(self._import_modules_from_package("data_access"))
        modules.update(self._import_modules_from_package("services"))
        modules.update(self._import_modules_from_package("helpers"))

        for module_name, module in modules.items():
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):
                    self.dependencies[attr_name] = attr()

    def resolve(self, class_name):
        """Bir sınıf için bağımlılıkları çözümler ve oluşturur."""
        cls = self.dependencies.get(class_name)
        if not cls:
            raise ValueError(f"{class_name} bulunamadı.")

        init_params = cls.__init__.__code__.co_varnames[1:]
        dependencies = {
            param: self.dependencies[param]
            for param in init_params
            if param in self.dependencies
        }

        return cls(**dependencies) if dependencies else cls

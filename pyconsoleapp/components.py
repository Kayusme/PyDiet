from abc import abstractmethod, ABC
from typing import Callable, Dict, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class ConsoleAppComponent(ABC):
    def __init__(self, app: 'ConsoleApp'):
        self.response_functions: Dict[str, Callable] = {}
        self.app = app

    def __getattribute__(self, name: str) -> Any:
        '''Intercepts the print command and adds the component to
        the app's list of active components.

        Arguments:
            name {str} -- Name of the attribute being accessed.

        Returns:
            Any -- The attribute which was requested.
        '''
        # If the print method was called;
        if name == 'print':
            # Add this component to the active components list
            self.app.activate_component(self)
        # Return whatever was requested;
        return super().__getattribute__(name)

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def print(self, *args, **kwargs) -> str:
        pass

    def set_response_function(self, signatures: List[str], func: Callable) -> None:
        for signature in signatures:
            self.response_functions[signature] = func
    
    def set_empty_response_function(self, func: Callable) -> None:
        self.set_response_function([''], func)

    def any_response(self, response:str) -> None:
        raise NotImplementedError

    # Deprecated
    def set_option_response(self, signature: str, func: Callable) -> None:
        self.response_functions[signature] = func

    # Deprecated
    def set_empty_enter_response(self, func:Callable)->None:
        self.response_functions[''] = func

    # Deprecated
    def dynamic_response(self, response: str) -> None:
        self.any_response(response)

    def run(self) -> None:
        pass


class ConsoleAppGuardComponent(ConsoleAppComponent):
    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)

    def clear_self(self):
        def search_and_clear_guard_map(guard_map):
            # Place to store guarded route to clear;
            rt_to_clear = None
            # Work through the entrance guard list looking for self;
            for route in guard_map.keys():
                # If found;
                if guard_map[route] == self:
                    # Delete entry from guard dict;
                    rt_to_clear = route
            if rt_to_clear:
                del guard_map[rt_to_clear]
        # Search and clear entrance & exit maps;
        search_and_clear_guard_map(self.app._route_entrance_guard_map)
        search_and_clear_guard_map(self.app._route_exit_guard_map)

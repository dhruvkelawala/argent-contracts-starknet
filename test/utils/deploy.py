import os
from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.compiler.compile import compile_starknet_files
from starkware.starknet.testing.state import StarknetState

compiled_code = {}

async def deploy(starknet, path, params=None):
    params = params or []
    if path in compiled_code:
        contract_definition = compiled_code[path]
    else:
        contract_definition = compile_starknet_files([path], debug_info=True)
        compiled_code[path] = contract_definition
    deployed_contract = await starknet.deploy(contract_def=contract_definition,constructor_calldata=params)
    return deployed_contract

async def deploy_proxy(starknet, proxy_path, implementation_path, params=None):
    params = params or []
    proxy_definition = compile_starknet_files([proxy_path], debug_info=True)
    implementation_definition = compile_starknet_files([implementation_path], debug_info=True)
    deployed_proxy = await starknet.deploy(contract_def=proxy_definition,constructor_calldata=params)
    wrapped_proxy = StarknetContract(
        state=starknet.state,
        abi=implementation_definition.abi,
        contract_address=deployed_proxy.contract_address,
        deploy_execution_info=deployed_proxy.deploy_execution_info)
    return wrapped_proxy
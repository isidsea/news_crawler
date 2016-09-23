from lib.converter_engine.interface import ConverterInterface

if __name__ == "__main__":
	print("[convert][debug] Converting...")
	ConverterInterface.multiple_convert_and_save()
	print("[convert][debug] Converted!")
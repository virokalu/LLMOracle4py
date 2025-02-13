from dotenv import load_dotenv

from models.doc import Doc
from services.docExtract import read_file_content, extract_docstring
from services.handlePrograms import get_names, run_program
from services.handleTestCases import get_inputs

# Load environment variables
load_dotenv()


def main():

    program_path = "QuixBugs"
    py_path = "python_programs"
    test_path = "json_testcases"

    # Get the names of the programs that testcases are available
    programs_names = get_names(program_path+"/json_testcases")

    for program_name in programs_names:
        print(f"{program_name}\n")

        """ Getting TestCases """
        num_lines, content = get_inputs(program_path+"/"+test_path+"/"+program_name+".json")

        """ Read File Content """
        doc_content = extract_docstring(read_file_content(program_path + "/" + py_path + "/" + program_name + ".py"))

        """ Extract the prompt Items """
        doc = Doc(doc_content)
        print(f"{doc.sections}\n")
        doc.print_sections()
        print("==================================================================================")

        # for i, item in enumerate(content, start=1):
        #     if isinstance(item, list) and len(item) == 2:
        #         input_, output_ = item  # Extract input and output elements
        #
        #         """ Running the Program """
        #         print(f"\nLine {input_[0]}")
        #         output, error = run_program(program_path + "/" + py_path + "/" + program_name + ".py", str(input_[0]))
        #
        #         if output is not None:
        #             print("Output of program " + program_name + f" ------------------------> {output_}")
        #         if error is not None:
        #             print("\nError on program " + program_name + " ------------------------>! " + error)
        #
        #     else:
        #         print(f"Line {i}: Error - Invalid format in {program_name}")


if __name__ == "__main__":
    main()

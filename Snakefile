rule run_injection:
	input:
		lambda wildcards: f"data/data_{int(wildcards.index):03d}.txt"
	output:
		directory("output_{index}")
	conda:
		"environment.yml"
	shell:
		"""
		python ./bin/fit_data.py --run_id {wildcards.index} --data_dir data --output_dir {output}
		"""
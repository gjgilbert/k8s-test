rule all:
	input:
		[f"output_{index}" for index in range(2)]

rule tests:
	#input:
	#	lambda wildcards: f"data/data_{int(wildcards.index):03d}.txt"
	output:
		directory("output_{index}")
	conda:
		"environment.yml"
	threads: 1
	resources:
		mem_mb=1000,
		disk_mb=1000
	shell:
		"""
		python ./bin/fit_data.py --run_id {wildcards.index} --data_dir data --output_dir {output}
		"""
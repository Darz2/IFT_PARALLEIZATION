using DataFrames, CSV

#pwd()
#cd("/scratch/darshanraju/A5/CO2")
#pwd()

data_pr = CSV.read("massdens_profile.dat", DataFrame; skipto=5, delim=' ', header=false)
select!(data_pr, Not([4]))
select!(data_pr, Not([2]))
select!(data_pr, Not([1]))
data_cleaned = dropmissing(data_pr)
column_names = names(data_cleaned)
rename!(data_cleaned, :Column3 => :Column1, :Column5 => :Column2, :Column6 => :Column3)

data_pr = data_cleaned
indices = unique(data_pr.Column1)
grouped = groupby(data_pr, :Column1)

new_data = DataFrame()
for i in 1:length(grouped)
    new_data[!, Symbol("group", i)] = grouped[i][!, :Column3]
end

insertcols!(new_data, 1, :Index => Int.(1e4 .* (1:size(new_data, 1))))

CSV.write("dens.csv", new_data)
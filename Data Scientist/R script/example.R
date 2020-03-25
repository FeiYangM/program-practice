#!/usr/bin/env Rscript

################################################################################
#usage: Rscript example.R inputfile                                            #
#output: inputfile.pdf                                                         #
#                                                                              #
#        plot distribution of mutation number, pliody state and rho number     #
#        in one figure                                                         #
#                                                                              #
################################################################################

library(ggplot2)

# read data file
args <- commandArgs(trailingOnly = TRUE)

# load data, transform and order
x <- read.table(args[1], sep = '\t', header = T, row.names = 1, check.names = F)
y <- t(x)
z <- y[order(y[,1], decreasing = T),]

# distribute values to variables
mutation <- z[,1]
ploidy <- z[,2]
rho <- z[,3]

# create dataframe
dt <- data.frame(Sample = row.names(z), M = mutation, P = ploidy, R = rho)

len <- length(x[1,])
one_para <- rep(0, each = len) # used in the plot
output <- paste(args[1], "pdf", sep = ".") # output file
pdf(output)

# plot distribution of mutation number, pliody state and rho number in one figure
ggplot(dt)+
  geom_bar(aes(x = reorder(Sample, -M),y = M,fill = "Mut_n"), stat = "identity", width = 0.2) +
  geom_bar(aes(x = reorder(Sample, -M),y = a,fill= "Ploidy_n"), stat = "identity", width = 0.2)+
  ylab("TMB") + 
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7.5, color="black")) +
  geom_text(aes(x = reorder(Sample, -M), y = M,label = ploidy), vjust = -0.8, hjust = 0.5,  color = "black", size = 2.5) +
  geom_line(aes(x = reorder(Sample, -M), y = R * 300, group = 1, color = "Purity")) +
  scale_y_continuous(sec.axis = sec_axis(~./max(mutation), name = "Rho", breaks = seq(0,1,0.3))) +
  labs(fill = "", colour = "") +
  scale_fill_manual(values = c("grey", "white")) +
  theme(legend.position = "bottom", axis.title.x = element_blank()) + 
  labs(caption = "Sample") + 
  theme(plot.caption = element_text(hjust = 0.5, size = 15))
dev.off()




